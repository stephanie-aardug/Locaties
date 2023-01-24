# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Locatie Fieldservice Helpdesk',
    'version': '16.0.0.0',
    'summary': 'Bridge between Location FSM and Helpdesk',
    'description': """ 
            This module is used to pass the location field from a helpdesk ticket to a fieldservice task.
        """,
    'category': 'location',
    'author': 'Aardug, Arjan Rosman',
    'website': 'arosman@aardug.nl',
    'depends': ['locaties_helpdesk', 'locaties_fieldservice'],
    'data': [
        'views/helpdesk_views.xml'
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
