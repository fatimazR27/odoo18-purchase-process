# Odoo 18 - Purchase Process Management

## 📋 Description
Module de gestion du processus d'achat pour l'entreprise Point TP (Construction).
Gestion complète des demandes d'achat, chantiers, projets et workflow de validation.

## 🏗️ Fonctionnalités
- ✅ Gestion des Projets et Chantiers
- ✅ Demandes d'Achat Interne (DAI)
- ✅ Workflow de validation multi-niveaux
- ✅ Génération automatique des codes
- ✅ Suivi des réceptions

## 🚀 Installation
\`\`\`bash
# Cloner le repository
git clone https://github.com/fatimazR27/odoo18-purchase-process.git
cd odoo18-purchase-process

# Installer le module dans Odoo
# Copier le dossier addons/purchase_process dans vos addons Odoo
# Activer le module dans les paramètres Odoo
\`\`\`

## 📁 Structure du Module
\`\`\`
addons/purchase_process/
├── models/
│   ├── __init__.py
│   ├── demande_achat.py
│   └── check_models.py
├── views/
│   ├── demande_achat_views.xml
│   ├── project_views.xml
│   └── chantier_views.xml
├── security/
│   └── ir.model.access.csv
├── data/
│   └── sequence_data.xml
└── __manifest__.py
\`\`\`

## 👥 Contributeurs
- Fatima Z. - Développement principal

## 📄 Licence
Ce projet est sous licence OPL (Odoo Proprietary License v1.0)
