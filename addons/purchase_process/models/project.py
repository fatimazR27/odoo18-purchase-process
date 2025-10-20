from odoo import models, fields, api

class Project(models.Model):
    _name = 'purchase.process.project'
    _description = 'Projet'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nom du Projet', required=True)
    code = fields.Char(string='Code Projet', copy=False, readonly=True)
    localisation = fields.Char(string='Localisation')
    description = fields.Text(string='Description')
    date_debut = fields.Date(string='Date de Début')
    date_fin = fields.Date(string='Date de Fin Prévisionnelle')
    chantier_ids = fields.One2many('purchase.process.chantier', 'project_id', string='Chantiers')
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('in_progress', 'En Cours'),
        ('done', 'Terminé'),
        ('cancel', 'Annulé')
    ], string='État', default='draft')
    
    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Le code projet doit être unique!'),
    ]

    @api.model
    def create(self, vals):
        if not vals.get('code'):
            vals['code'] = self.env['ir.sequence'].next_by_code('purchase.process.project') or 'Nouveau'
        return super().create(vals)
