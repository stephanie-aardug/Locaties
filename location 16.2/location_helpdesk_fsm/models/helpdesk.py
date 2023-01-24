# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import models, fields, _


class HelpdeskCreateFsmTask(models.TransientModel):
    _inherit = 'helpdesk.create.fsm.task'

    x_aa_location_id = fields.Many2one('locatie.locatie', string='Location')

    def action_generate_task(self):
        task = super(HelpdeskCreateFsmTask, self).action_generate_task()
        task.x_aa_locatie_id = self.x_aa_location_id


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    def action_generate_fsm_task(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Create a Field Service task'),
            'res_model': 'helpdesk.create.fsm.task',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'use_fsm': True,
                'default_helpdesk_ticket_id': self.id,
                'default_user_id': False,
                'default_partner_id': self.partner_id.id if self.partner_id else False,
                'default_name': self.name,
                'default_project_id': self.team_id.fsm_project_id.id,
                'default_x_aa_location_id': self.x_aa_locatie_id.id if self.x_aa_locatie_id else False
            }
        }
