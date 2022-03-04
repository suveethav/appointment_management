# -*- coding: utf-8 -*-
{
    'name': 'Hospital Appointment Management',
    'version': '11.0',
    'license': 'LGPL-3',
    'category': 'Hospital Appointment Management',
    'summary': 'Manage Doctor & Patient Appointment',
    'complexity': "easy",
    'description': """
        This module provide Hospital Appointment Management.
    """,
    'author': 'Suveetha',
    'website': '',
    'depends': ['base'],
    'data': [
        'security/appointment_groups.xml',
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'views/appointment_view.xml',
        'views/res_doctor_view.xml',
        'views/res_patient_view.xml',
        'views/appointment_seq.xml',
        'wizard/approval_reject_wizard_view.xml',


    ],
    'images': [
        'static/description/icon.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
