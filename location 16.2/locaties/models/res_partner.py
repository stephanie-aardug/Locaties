# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _compute_user_lang(self):
        for rec in self:
            rec.user_lang = self.env['res.lang']._lang_get(self.env.user.lang).name

    user_lang = fields.Char(compute="_compute_user_lang")
    x_aa_location_count = fields.Integer(compute='_compute_location_count')
    type = fields.Selection(selection_add=[('location', 'Location Type')])

    def action_open_location_kanban(self):
        action = self.env["ir.actions.actions"]._for_xml_id("locaties.locatie_view_action")
        action['context'] = {}
        action['domain'] = [('partner_id', '=', self.ids)]
        action['view_mode'] = 'kanban'
        return action

    @api.model
    def _compute_location_count(self):
        for rec in self:
            rec.x_aa_location_count = len(self.env['locatie.locatie'].search([('partner_id', '=', rec.id)]))