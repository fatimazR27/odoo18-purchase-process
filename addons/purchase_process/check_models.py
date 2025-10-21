#!/usr/bin/env python3
import subprocess

# Vérifier les champs de chaque modèle
commands = [
    "docker exec odoo18-purchase /usr/bin/odoo shell -d FINAL --shell-interface=python << 'PYEOF'\n"
    "print('=== PROJECT FIELDS ===')\n"
    "for field in env['purchase.process.project'].fields_get():\n"
    "    print(f'  {field}')\n"
    "PYEOF",
    
    "docker exec odoo18-purchase /usr/bin/odoo shell -d FINAL --shell-interface=python << 'PYEOF'\n"
    "print('=== CHANTIER FIELDS ===')\n"
    "for field in env['purchase.process.chantier'].fields_get():\n"
    "    print(f'  {field}')\n"
    "PYEOF",
    
    "docker exec odoo18-purchase /usr/bin/odoo shell -d FINAL --shell-interface=python << 'PYEOF'\n"
    "print('=== DEMANDE ACHAT FIELDS ===')\n"
    "for field in env['purchase.process.demande.achat'].fields_get():\n"
    "    print(f'  {field}')\n"
    "PYEOF"
]

for cmd in commands:
    print("Exécution...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("ERREUR:", result.stderr)
