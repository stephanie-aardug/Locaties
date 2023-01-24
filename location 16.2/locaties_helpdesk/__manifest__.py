# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Locaties Helpdesk',
    'version': '16.0.0.0',
    'summary': 'Helpdesk Extension for locations',
    'description': """ 
        Module which adds support for locations on helpdesk.
        """,
    'category': 'location',
    'author': 'Aardug, Arjan Rosman',
    'website': 'arosman@aardug.nl',
    'depends': ['helpdesk', 'locaties'],
    'data': [
        'views/locatie_views.xml',
        'views/helpdesk_views.xml'
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
