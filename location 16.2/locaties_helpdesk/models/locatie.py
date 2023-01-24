# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import api, fields, models


class Locatie(models.Model):
    _inherit = 'locatie.locatie'

    @api.depends('partner_id')
    def _compute_helpdesk_ticket_count(self):
        ''' Method to compute kanban state'''

        helpdesk_ticket_obj = self.env["helpdesk.ticket"]
        for rec in self:
            rec.x_aa_helpdesk_ticket_count = 0
            tickets_recs = helpdesk_ticket_obj.search_count([('x_aa_locatie_id', '=', rec.id)])
            rec.x_aa_helpdesk_ticket_count = tickets_recs

    x_aa_helpdesk_ticket_count = fields.Integer(compute="_compute_helpdesk_ticket_count")

    def action_open_helpdesk_ticket(self):
        '''this method is redirect the current records
        helpdesk ticket view from smart button'''

        action = self.env["ir.actions.actions"]._for_xml_id(
            "helpdesk.helpdesk_ticket_action_main_my")
        tickets = self.env['helpdesk.ticket'].search([
            ('x_aa_locatie_id', '=', self.id)])
        action['domain'] = [('id', 'in', tickets.ids)]
        action['context'] = dict(
            self._context,
            default_x_aa_locatie_id=self.id
        )
        return action
