# -*- coding: utf-8 -*-
{
    "name": "questions generation",
    "summary": """
        questions generation test""",
    "description": """
        A combination of an eLearning app and Automatic Question Generation. 
Automatic Question Generation (AQG) is the technique for generating a right set of questions from a content. Question Generators use trained machine learning algorithms to generate questions using some text information as the input. Given information is processed through the neural networks as a hidden step. As the output, we get questions with different variants of answers.

    """,
    "author": "Sprinterra",
    "license": 'LGPL-3',
    "website": "https://www.sprinterra.com/",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "website_slides"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/qgen_views.xml",
        "views/templates.xml",
        "views/slide_view.xml",
        "views/res_config_settings_view.xml",
    ],
    "images": ['static/description/assets.gif'],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
}
