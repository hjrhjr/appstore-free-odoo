# -*- coding: utf-8 -*-

from .third.MQA_QG.Operators import T5_QG
from odoo import models, fields

from Questgen import main

from . import pipelines
from textblob import TextBlob
import logging
import random
import nltk

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
_logger = logging.getLogger(__name__)
import sys

_logger.info(sys.path)


class QGen(models.Model):
    _name = "slide.qgen"
    _description = "quetion generation"

    name = fields.Char(string="Content name")
    origin = fields.Text(string="Text to generate questions")
    channel_name = fields.Many2one("slide.channel", string="Course name", required=True)
    result = fields.Text(string="Result")
    slide_name = fields.Many2one(
        "slide.slide",
        string="Content name",
        required=True,
        domain='[("channel_id", "=", channel_name)]',
    )
    ml_name = fields.Selection(
        selection="_edit_ml_name",
        string="",
    )

    def _edit_ml_name(self):
        res = []
        if (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("slide.qgen.settings.container.question_generation")
            == "True"
        ):
            res.append(("question_generation", "PATIL-SURAJ"))
        if (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("slide.qgen.settings.container.questgen")
            == "True"
        ):
            res.append(("Questgen.ai", "QUESTGEN"))
        if (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("slide.qgen.settings.container.teacherpeterpan")
            == "True"
        ):
            res.append(("teacherpeterpan", "MQA-QG"))
        return res

    ml_type = fields.Selection(
        [
            ("qe", "Yes/No"),
            ("qg", "MCQ Questions"),
        ],
        string="",
    )
    spliter_type = fields.Selection(
        string="How to split?",
        selection="_edit_sliter_type",
    )

    def _edit_sliter_type(self):
        return [
            ("sent", "Sentence"),
            ("paragraph", "Paragraph"),
            ("custom", "Custom"),
        ]

    spliter = fields.Char(
        string="Splitter Symbol",
        default="----------------------------------------------",
    )
    question_ids = fields.One2many(
        "slide.question", "gen_q_id", string="Questions", readonly=False
    )

    def question_generation(self, nlp):
        res = []
        for seq in self.origin.split(self.spliter):
            if len(seq) < 10:
                continue
            try:
                quizs = nlp(seq)
                for quiz in quizs:
                    res.append(
                        {
                            "q": quiz["question"],
                            "context": seq,
                            "a": [
                                {"text": quiz["answer"], "true": True},
                                {
                                    "text": "Not a {}".format(quiz["answer"].lower()),
                                    "true": False,
                                },
                            ],
                        }
                    )
            except:
                _logger.error("Problem with:")
                _logger.error(seq)
                continue
        return res

    def quesgen_ai_bool(self, qe):
        # Generate boolean (Yes/No) Questions, now it's random
        res = []

        for seq in self.origin.split(self.spliter):
            output = qe.predict_boolq({"input_text": seq})
            for quiz in output["Boolean Questions"]:
                res.append(
                    {
                        "q": quiz,
                        "context": output["Text"],
                        "a": [
                            {"text": "Yes", "true": False},
                            {"text": "No", "true": True},
                        ],
                    }
                )
        return res

    def quesgen_ai_multi(self, qg):
        # Generate multiselect questions
        res = []
        # just write general generator
        if not self.spliter:
            spliter = None
        else:
            spliter = self.spliter
        for seq in self.origin.replace("\n", "").split(spliter):
            if not seq:
                continue
            output = qg.predict_mcq({"input_text": seq})
            for quiz in output["questions"]:
                answers = []
                for ans in quiz["options"]:
                    answers.append({"text": ans, "true": False})
                answers.append({"text": quiz["answer"], "true": True})
                random.shuffle(answers)
                res.append(
                    {
                        "q": quiz["question_statement"],
                        "context": quiz["context"],
                        "a": answers,
                    }
                )

        return res

    def quesgen_simple(self):
        wiki = TextBlob(self.origin)
        tags = wiki.tags
        htags = []
        for tag in tags:
            htags.append((tag[0], "({}) {}".fromat(tag[1], HL_TAGS[tag[1]])))
        self.result = str(htags)

    def teacherpeterpan(self, nlp):
        res = []
        if not self.spliter:
            spliter = None
        else:
            spliter = self.spliter
        for seq in self.origin.replace("\n", "").split(spliter):
            questions = nlp.qg_without_answer(seq)
            for quiz in questions:
                res.append(
                    {
                        "q": quiz["question"],
                        "context": seq,
                        "a": [
                            {"text": quiz["answer"], "true": True},
                            {
                                "text": "Not a {}".format(quiz["answer"].lower()),
                                "true": False,
                            },
                        ],
                    }
                )
            del questions
        return res

    def gen_question_generation(self):
        if self.spliter_type == "sent":
            self.spliter = "."
        elif self.spliter_type == "paragraph":
            self.spliter = ".\n"
        if self.ml_name == "question_generation":
            nlp = pipelines.pipeline("question-generation")
            qag = self.question_generation(nlp)
            del nlp
        elif self.ml_name == "teacherpeterpan":
            nlp = T5_QG.pipeline(
                "question-generation",
                model="valhalla/t5-base-qg-hl",
                qg_format="highlight",
            )
            qag = self.teacherpeterpan(nlp)
            del nlp
        elif self.ml_name == "Questgen.ai":
            if self.ml_type == "qe":
                qe = main.BoolQGen()
                qag = self.quesgen_ai_bool(qe)
                del qe
            elif self.ml_type == "qg":
                qg = main.QGen()
                qag = self.quesgen_ai_multi(qg)
                del qg
        elif self.ml_name == "SimleQ":
            self.quesgen_simple()
            return
        self.name = self.slide_name.name
        for quiz in qag:
            q_id = self.env["slide.question"].create(
                {
                    "question": quiz["q"],
                    "context": quiz["context"],
                    "slide_id": self.slide_name[0].id,
                    "gen_q_id": self.id,
                }
            )
            for answer in quiz["a"]:
                self.env["slide.answer"].create(
                    {
                        "text_value": answer["text"],
                        "comment": quiz["context"],
                        "question_id": q_id.id,
                        "is_correct": answer["true"],
                    }
                )
        self.result = str(qag)

    def del_questions_and_content(self):
        for q in self.question_ids:
            q.unlink()
        self.slide_name.unlink()
