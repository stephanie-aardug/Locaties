# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    x_aa_locatie_id = fields.Many2one(
        'locatie.locatie',
        string='Location'
    )
    x_aa_equipment_id = fields.Many2one(
        'maintenance.equipment',
        string='Equipment'
    )
    x_aa_partner_id = fields.Integer(related='x_aa_locatie_id.partner_id.id')
    x_aa_location_partner_id = fields.Integer(related='x_aa_locatie_id.x_aa_location_partner_id.id')
