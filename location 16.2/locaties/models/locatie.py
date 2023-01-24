# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import api, fields, models, _


class Locatie(models.Model):
    _name = 'locatie.locatie'
    _description = 'Location'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_default_stage_id(self):
        '''To get default stage'''
        locatie_stages = self.env['locatie.stage'].search([])
        return locatie_stages[0] if locatie_stages else False

    @api.depends('x_aa_stage_id')
    def _compute_kanban_state(self):
        '''Method to compute kanban state'''
        stage_new = self.env.ref('locaties.event_stage_new', raise_if_not_found=False)
        stage_inprogress = self.env.ref('locaties.event_stage_intreatment', raise_if_not_found=False)
        stage_done = self.env.ref('locaties.event_stage_ready', raise_if_not_found=False)
        stage_cancel = self.env.ref('locaties.event_stage_cancel', raise_if_not_found=False)
        for rec in self:
            rec.x_aa_kanban_state = 'draft'
            if rec.x_aa_stage_id.id == stage_new.id:
                rec.x_aa_kanban_state = 'draft'
            elif rec.x_aa_stage_id.id == stage_inprogress.id:
                rec.x_aa_kanban_state = 'normal'
            elif rec.x_aa_stage_id.id == stage_done.id:
                rec.x_aa_kanban_state = 'done'
            elif rec.x_aa_stage_id.id == stage_cancel.id:
                rec.x_aa_kanban_state = 'blocked'

    @api.depends('partner_id')
    def _compute_maintenance_equipment_count(self):
        ''' Method to compute maintenance equipment count '''
        maintenance_equipment_obj = self.env["maintenance.equipment"]
        for rec in self:
            rec.x_aa_maintenance_equipment_count = 0
            equipment_recs = maintenance_equipment_obj.search_count([('x_aa_locatie_id', '=', rec.id)])
            rec.x_aa_maintenance_equipment_count = equipment_recs

    @api.depends('partner_id')
    def _compute_maintenance_request_count(self):
        ''' Method to compute maintenance request count'''
        maintenance_request_obj = self.env["maintenance.request"]
        for rec in self:
            rec.x_aa_maintenance_request_count = 0
            maintenance_request_recs = maintenance_request_obj.search_count([('x_aa_locatie_id', '=', rec.id)])
            rec.x_aa_maintenance_request_count = maintenance_request_recs

    # -- Base Info -- #
    name = fields.Char('Name')
    active = fields.Boolean(default=True)
    priority = fields.Boolean("Priority")
    x_aa_stage_id = fields.Many2one(
        'locatie.stage',
        ondelete='restrict',
        default=_get_default_stage_id,
        domain='[("active", "=", True)]',
        tracking=True,
        group_expand='_read_group_expand_full',
        string="Stage"
    )
    x_aa_kanban_state = fields.Selection([
        ('draft', 'New'),
        ('normal', 'In Progress'),
        ('done', 'Done'),
        ('blocked', 'Blocked')],
        compute='_compute_kanban_state',
        string="State"
    )
    x_aa_maintenance_equipment_count = fields.Integer(compute="_compute_maintenance_equipment_count")
    x_aa_maintenance_request_count = fields.Integer(compute="_compute_maintenance_request_count")

    # -- Customer Information -- #
    partner_id = fields.Many2one(
        'res.partner',
        string="Contact",
        tracking=True
    )
    x_aa_partner_phone = fields.Char('Telephone', tracking=True)
    x_aa_partner_email = fields.Char('E-mail', tracking=True)

    # -- Responsible, Tags -- #
    responsible_id = fields.Many2one(
        'res.partner',
        string='Responsible'
    )
    x_aa_tag_ids = fields.Many2many(
        'locatie.tag',
        'locatie_tag_rel',
        'locatie_id', 'tag_id',
        string='Location Tags'
    )

    # -- Location -- #
    x_aa_location_partner_id = fields.Many2one('res.partner', string='Location Contact')
    x_aa_street = fields.Char(related='x_aa_location_partner_id.street')
    x_aa_zip = fields.Char(related='x_aa_location_partner_id.zip')
    x_aa_city = fields.Char(related='x_aa_location_partner_id.city')
    x_aa_state_id = fields.Many2one(related='x_aa_location_partner_id.state_id')
    x_aa_country_id = fields.Many2one(related='x_aa_location_partner_id.country_id')
    x_aa_photo = fields.Binary(string="Photo")

    # -- Installation -- #
    x_aa_notes = fields.Html("Install information")
    x_aa_electricity_supply = fields.Char("Electricity supply")

    # -- Maintenance Information -- #
    x_aa_maintenance_information = fields.Html("Maintenance information")

    # -- Photos -- #
    x_aa_photo_1 = fields.Binary("Photo 1")
    x_aa_photo_1_1 = fields.Binary("Photo 1")
    x_aa_photo_2 = fields.Binary("Photo 2")
    x_aa_photo_2_1 = fields.Binary("Photo 2")
    x_aa_photo_3 = fields.Binary("Photo 3")
    x_aa_photo_3_1 = fields.Binary("Photo 3")

    # -- Opening hours -- #
    x_aa_is_open_full_day = fields.Boolean("Open 24 hours a day")
    x_aa_opening_hours = fields.Text("Opening hours during the week:")

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.write({
                'x_aa_partner_phone': self.x_aa_location_partner_id.phone,
                'x_aa_partner_email': self.x_aa_location_partner_id.email,
            })

    def action_open_maintenance_equipment(self):
        '''this method is redirect the current records
        maintenance equipment view from amrt button'''
        action = self.env["ir.actions.actions"]._for_xml_id(
            "maintenance.hr_equipment_action")
        equipments = self.env['maintenance.equipment'].search([
            ('x_aa_locatie_id', '=', self.id)])
        action['domain'] = [('id', 'in', equipments.ids)]
        action['context'] = dict(
            self._context,
            default_x_aa_locatie_id=self.id
        )
        return action

    def action_open_maintenance_request(self):
        '''this method is redirect the current records
        maintenance request view from amrt button'''
        action = self.env["ir.actions.actions"]._for_xml_id(
            "maintenance.hr_equipment_request_action")
        maintenances = self.env['maintenance.equipment'].search([
            ('x_aa_locatie_id', '=', self.id)])
        action['domain'] = [('id', 'in', maintenances.ids)]
        action['context'] = dict(
            self._context,
            default_x_aa_locatie_id=self.id
        )
        return action
