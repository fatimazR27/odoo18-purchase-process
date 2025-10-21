from odoo import models, fields, api
from odoo.exceptions import UserError

class DemandeAchat(models.Model):
    _name = 'purchase.process.demande.achat'
    _description = 'Demande d\'Achat'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Référence', copy=False, readonly=True, default='Nouveau')
    chantier_id = fields.Many2one('purchase.process.chantier', string='Chantier', required=True, tracking=True)
    project_id = fields.Many2one('purchase.process.project', string='Projet', related='chantier_id.project_id', store=True, tracking=True)
    article = fields.Char(string='Article/Service', required=True, tracking=True)
    description = fields.Text(string='Description Détaillée')
    quantite = fields.Float(string='Quantité', required=True, default=1.0, tracking=True)
    
    unite_mesure = fields.Selection([
        ('unite', 'Unité'),
        ('kg', 'Kilogramme'),
        ('g', 'Gramme'),
        ('tonne', 'Tonne'),
        ('litre', 'Litre'),
        ('ml', 'Millilitre'),
        ('m', 'Mètre'),
        ('cm', 'Centimètre'),
        ('m2', 'Mètre Carré'),
        ('m3', 'Mètre Cube'),
        ('paquet', 'Paquet'),
        ('carton', 'Carton'),
        ('sachet', 'Sachet'),
        ('rouleau', 'Rouleau'),
        ('heure', 'Heure'),
        ('jour', 'Jour'),
        ('mois', 'Mois')
    ], string='Unité de Mesure', default='unite', required=True, tracking=True)
    
    urgence = fields.Selection([
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
        ('tres_urgent', 'Très Urgent')
    ], string='Niveau d\'Urgence', default='normal', tracking=True)
    
    date_besoin = fields.Date(string='Date de Besoin', required=True, tracking=True)
    chef_chantier_id = fields.Many2one('res.users', string='Demandeur', default=lambda self: self.env.user, tracking=True)
    
    state = fields.Selection([
        ('draft', 'Brouillon'),
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
        if not vals.get('name') or vals.get('name') == 'Nouveau':
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.process.demande.achat') or 'Nouveau'
        return super().create(vals)

    def action_envoyer_validation(self):
        """Send for technical validation - Brouillon → Validation Technique"""
        for record in self:
            if record.state == 'draft':
                record.write({'state': 'technical_validation'})
                record.message_post(body="Demande envoyée en validation technique")
        return True

    def action_valider_technique(self):
        """Validate technically - Validation Technique → Approuvé"""
        for record in self:
            if record.state == 'technical_validation':
                record.write({
                    'state': 'approved',
                    'directeur_technique_id': self.env.user.id,
                    'date_validation_technique': fields.Datetime.now()
                })
                record.message_post(body="Demande validée techniquement")
        return True

    def action_rejeter(self):
        """Reject and return to draft"""
        for record in self:
            record.write({'state': 'draft'})
            record.message_post(body="Demande rejetée")
        return True

    def action_creer_bon_commande(self):
        """Create purchase order - Approuvé → Bon de Commande Créé"""
        for record in self:
            if record.state == 'approved':
                record.write({'state': 'purchase_order'})
                record.message_post(body="Bon de commande créé")
        return True

    def action_valider_reception(self):
        """Validate reception - Bon de Commande → Réceptionné"""
        for record in self:
            if record.state == 'purchase_order':
                record.write({
                    'state': 'received',
                    'date_reception': fields.Datetime.now(),
                    'responsable_reception': self.env.user.id
                })
                record.message_post(body="Réception validée")
        return True

    def action_terminer(self):
        """Mark as done - Réceptionné → Terminé"""
        for record in self:
            if record.state == 'received':
                record.write({'state': 'done'})
                record.message_post(body="Processus d'achat terminé")
        return True

    def action_annuler(self):
        """Cancel the demand"""
        for record in self:
            record.write({'state': 'cancel'})
            record.message_post(body="Demande annulée")
        return True
