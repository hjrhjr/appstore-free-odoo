# -*- coding: utf-8 -*-

import logging

_logger = logging.getLogger(__name__)
# import sys

# sys.path.append("/home/ubuntu/addons/f/Unsupervised-Multi-hop-QA")
from .third.MQA_QG.Operators import T5_QG
from odoo import models, fields, api
from Questgen import main

from . import pipelines
import random
import nltk

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
PARAMS = [
    ("question_generation", "slide.qgen.settings.container.question_generation"),
    ("questgen", "slide.qgen.settings.container.questgen"),
    ("teacherpeterpan", "slide.qgen.settings.container.teacherpeterpan"),
]


class GenQuestions(models.Model):
    _inherit = "slide.question"
    _description = "add field for gen_q1"

    gen_q_id = fields.Many2one("slide.qgen", string="")
    context = fields.Text(string="Context")


# class GenChannel(models.Model):
#     """A channel is a container of slides."""

#     _inherit = "slide.channel"

#     name = fields.Char("Name", translate=True, required=True, store=True)

#     @api.onchange("name")
#     def _onchange_name(self):
#         # self.name = "Channel name"
#         self.create({"name": "name"})
#         action_id = self.env.ref("website_slides.slide_channel_action_overview").read()[
#             0
#         ]
#         _logger.info(action_id)
#         if action_id:
#             action_id["res_id"] = self.id
#         return action_id


class GenAnswers(models.Model):
    _inherit = "slide.answer"
    _description = "add field for gen_q1"

    @api.onchange("comment", "text_value")
    def _onchange_comment(self):
        if not self.comment:
            for ans in self.question_id.answer_ids:
                if ans.comment:
                    self.comment = ans.comment


class GenContent(models.Model):
    _inherit = "slide.slide"
    _description = "Slides"

    generate = fields.Boolean(string="Question generator")
    origin = fields.Text(string="Text to generate questions")
    result = fields.Text(string="Result")
    channel_id = fields.Many2one("slide.channel", string="Course", required=True)
    ml_name = fields.Selection(
        selection="_edit_ml_name",
        string="Neural Network",
    )
    spliter = fields.Char(
        string="Splitter Symbol",
        default="----------------------------------------------",
    )
    ml_type = fields.Selection(
        [
            ("qe", "Yes/No"),
            ("qg", "MCQ Questions"),
        ],
        string="Question Type",
    )
    spliter_type = fields.Selection(
        string="Splitter Option", selection="_edit_sliter_type", default="full"
    )
    my_button = fields.Boolean("Label")

    @api.onchange("channel_id")
    def onchange_my_button(self):
        for record in self:
            _logger.info
            if isinstance(self.channel_id.id, models.NewId):
                default_channel = self.env["slide.channel"].search([])
                self.channel_id = default_channel[0].id
                _logger.info("simple" * 88)
                _logger.info(self.id)
                _logger.info(self._origin.id)
                _logger.info(self.question_ids)
                _logger.info(self._origin.question_ids)

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

    def _edit_sliter_type(self):
        return [
            ("sent", "Sentence"),
            ("paragraph", "Paragraph"),
            ("custom", "Custom"),
            ("full", "Full"),
        ]

    def question_generation(self, nlp):
        res = []
        _logger.info(self.spliter)
        _logger.info(self.origin)
        _logger.info("question_generation")
        if not self.spliter:
            spliter, count = None, 0
        else:
            spliter, count = self.spliter, -1
        for seq in self.origin.split(spliter, count):
            _logger.info(seq)
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
        if not self.spliter:
            spliter, count = None, 0
        else:
            spliter, count = self.spliter, -1
        for seq in self.origin.split(spliter, count):
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
            spliter, count = None, 0
        else:
            spliter, count = self.spliter, -1
        for seq in self.origin.split(spliter, count):
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

    def teacherpeterpan(self, nlp):
        res = []
        if not self.spliter:
            spliter, count = None, 0
        else:
            spliter, count = self.spliter, -1
        for seq in self.origin.split(spliter, count):
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
        _logger.info("gen_question_generation")
        _logger.info("simple" * 88)
        if self.spliter_type == "sent":
            self.spliter = "."
        elif self.spliter_type == "paragraph":
            self.spliter = ".\n"
        elif self.spliter_type == "full":
            self.spliter = False
        else:
            self.spliter = False
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
        else:
            return
        # save question with onchange
        # for quiz in qag:
        #     data = {
        #         "question": quiz["q"],
        #         "context": quiz["context"],
        #         "slide_id": self.id,
        #     }
        #     _logger.info(data)
        #     self.question_ids = [(0, False, data)]
        #     _logger.info(quiz["a"])
        #     _logger.info(self.question_ids[-1].answer_ids)
        #     _logger.info(self.question_ids[-1].id)
        #     # q_id = self.question_ids.create(data)
        #     for answer in quiz["a"]:
        #         a_data = {
        #             "text_value": answer["text"],
        #             "comment": quiz["context"],
        #             "question_id": self.question_ids[-1].id,
        #             "is_correct": answer["true"],
        #         }
        #         self.question_ids[-1].update({"answer_ids": [(0, False, a_data)]})
        #     _logger.info("after")
        #     _logger.info(self.question_ids[-1].answer_ids)
        #     _logger.info(self.question_ids[-1].id)

        for quiz in qag:
            data = {
                "question": quiz["q"],
                "context": quiz["context"],
                "slide_id": self.id,
            }
            _logger.info(data)
            _logger.info(quiz["a"])
            q_id = self.question_ids.create(data)
            _logger.info(q_id)
            for answer in quiz["a"]:
                a_data = {
                    "text_value": answer["text"],
                    "comment": quiz["context"],
                    "question_id": q_id.id,
                    "is_correct": answer["true"],
                }
                q_id.answer_ids.create(a_data)
        self.result = str(qag)

    def del_questions_and_content(self):
        for q in self.question_ids:
            q.unlink()
