# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Hospital management',
    'version': '1.0.0',
    'category': 'Hsopital',
    'sequence': '-100',

    'summary': 'Hospital Management System',
    'description': """Hsopital Management System
    """,
    'depends': ['mail', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'data1/sequence.xml',
        'wizards/cancel_appointment_view.xml',
        'views/menu.xml',
        'views/patient_view.xml',
        'views/female_patient_view.xml',
        'views/appointment_view.xml',
        'views/odoo_playground_view.xml',
        'views/patient_tag_view.xml',
        'views/res_config_settings_views.xml',



    ],
    'demo': [],
    'application': True,
    'auto_install': False,

    'license': 'LGPL-3',
}
