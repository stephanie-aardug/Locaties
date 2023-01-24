# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import api, fields, models


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    x_aa_locatie_id = fields.Many2one(
        'locatie.locatie',
        string='Location'
    )
    x_aa_location_customer_id = fields.Many2one(
        related='x_aa_locatie_id.partner_id', string='Customer', store=True
    )
    x_aa_specific_location = fields.Char(
        string='Specific Location'
    )


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    x_aa_locatie_id = fields.Many2one(
        'locatie.locatie',
        string='Location'
    )