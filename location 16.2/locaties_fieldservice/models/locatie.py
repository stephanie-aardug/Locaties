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

    def _compute_fieldservice_task_count(self):
        ''' Method to compute kanban state'''

        fieldservice_task_obj = self.env["project.task"]
        for rec in self:
            rec.x_aa_fieldservice_task_count = 0
            task_recs = fieldservice_task_obj.search_count([('x_aa_locatie_id', '=', rec.id)])
            rec.x_aa_fieldservice_task_count = task_recs

    x_aa_fieldservice_task_count = fields.Integer(compute="_compute_fieldservice_task_count")

    def action_open_fieldservice_task(self):
        '''this method is redirect the current records
        fieldservice task view from smart button'''

        action = self.env["ir.actions.actions"]._for_xml_id(
            "industry_fsm.project_task_action_fsm")
        tasks = self.env['project.task'].search([
            ('x_aa_locatie_id', '=', self.id)])
        action['domain'] = [('id', 'in', tasks.ids)]
        action['context'] = dict(
            self._context,
            default_x_aa_locatie_id=self.id
        )
        return action
