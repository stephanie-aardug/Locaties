# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Locaties Fieldservice',
    'version': '16.0.0.0',
    'summary': 'Fieldservice Extension for locations',
    'description': """ 
        Module which adds support for locations on fieldservice.
        """,
    'category': 'location',
    'author': 'Aardug, Arjan Rosman',
    'website': 'arosman@aardug.nl',
    'depends': ['industry_fsm', 'locaties'],
    'data': [
        'views/locatie_views.xml',
        'views/project_task_views.xml'
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
