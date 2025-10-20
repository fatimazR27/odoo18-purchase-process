from odoo import models, fields, api
from odoo.exceptions import UserError

class DemandeAchat(models.Model):
    _name = 'purchase.process.demande.achat'
    _description = 'Demande d\'Achat'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Référence', copy=False, readonly=True)
    chantier_id = fields.Many2one('purchase.process.chantier', string='Chantier', required=True)
    project_id = fields.Many2one('purchase.process.project', string='Projet', related='chantier_id.project_id', store=True)
    article = fields.Char(string='Article/Service', required=True)
    description = fields.Text(string='Description Détaillée')
    quantite = fields.Float(string='Quantité', required=True, default=1.0)
    unite_mesure = fields.Char(string='Unité de Mesure', default='Unité')
    urgence = fields.Selection([
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
        ('tres_urgent', 'Très Urgent')
    ], string='Niveau d\'Urgence', default='normal')
    date_besoin = fields.Date(string='Date de Besoin', required=True)
    chef_chantier_id = fields.Many2one('res.users', string='Demandeur', default=lambda self: self.env.user)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('sent', 'Envoyé'),
        ('technical_validation', 'Validation Technique'),
        ('approved', 'Approuvé'),
        ('purchase_order', 'Bon de Commande Créé'),
        ('received', 'Réceptionné'),
        ('done', 'Terminé'),
        ('cancel', 'Annulé')
    ], string='État', default='draft', tracking=True)
    
    # Validation workflow
    directeur_technique_id = fields.Many2one('res.users', string='Directeur Technique')
    date_validation_technique = fields.Datetime(string='Date Validation Technique')
    notes_validation = fields.Text(string='Notes de Validation')
    
    # Related purchase order
    purchase_order_id = fields.Many2one('purchase.order', string='Bon de Commande Associé')
    
    # Reception fields
    date_reception = fields.Datetime(string='Date Réception')
    responsable_reception = fields.Many2one('res.users', string='Responsable Réception')
    notes_reception = fields.Text(string='Notes Réception')
    
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'La référence de demande d\'achat doit être unique!'),
    ]

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.process.demande.achat') or 'Nouveau'
        return super().create(vals)

    def action_envoyer_validation(self):
        for record in self:
            if record.state == 'draft':
                record.write({'state': 'technical_validation'})

    def action_valider_technique(self):
        for record in self:
            if record.state == 'technical_validation':
                record.write({
                    'state': 'approved',
                    'directeur_technique_id': self.env.user.id,
                    'date_validation_technique': fields.Datetime.now()
                })

    def action_rejeter(self):
        for record in self:
            record.write({'state': 'draft'})

    def action_creer_bon_commande(self):
        for record in self:
            if record.state == 'approved':
                # Create a simple purchase order (you can enhance this)
                purchase_order = self.env['purchase.order'].create({
                    'partner_id': 1,  # Default supplier, should be selected
                    'order_line': [(0, 0, {
                        'name': record.article,
                        'product_qty': record.quantite,
                        'price_unit': 0.0,  # Should be set properly
                    })]
                })
                record.write({
                    'state': 'purchase_order',
                    'purchase_order_id': purchase_order.id
                })

    def action_valider_reception(self):
        for record in self:
            if record.state == 'purchase_order':
                record.write({
                    'state': 'received',
                    'date_reception': fields.Datetime.now(),
                    'responsable_reception': self.env.user.id
                })
    
    # Methods for button visibility (will be used in views)
    def show_send_validation_button(self):
        return self.state == 'draft'
    
    def show_validate_technical_button(self):
        return self.state == 'technical_validation'
    
    def show_create_order_button(self):
        return self.state == 'approved'
    
    def show_validate_reception_button(self):
        return self.state == 'purchase_order'
    
    def show_reject_button(self):
        return self.state in ['technical_validation', 'approved']
