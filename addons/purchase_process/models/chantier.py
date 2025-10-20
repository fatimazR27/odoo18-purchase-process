from odoo import models, fields, api

class Chantier(models.Model):
    _name = 'purchase.process.chantier'
    _description = 'Chantier'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nom du Chantier', required=True)
    code = fields.Char(string='Code Chantier', copy=False, readonly=True)
    project_id = fields.Many2one('purchase.process.project', string='Projet', required=True)
    localisation = fields.Char(string='Localisation')
    chef_chantier = fields.Many2one('res.users', string='Chef de Chantier')
    conducteur_travaux = fields.Many2one('res.users', string='Conducteur de Travaux')
    description = fields.Text(string='Description')
    demande_achat_ids = fields.One2many('purchase.process.demande.achat', 'chantier_id', string='Demandes d\'Achat')
    
    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Le code chantier doit être unique!'),
    ]

    @api.model
    def create(self, vals):
        if not vals.get('code'):
            vals['code'] = self.env['ir.sequence'].next_by_code('purchase.process.chantier') or 'Nouveau'
        return super().create(vals)
