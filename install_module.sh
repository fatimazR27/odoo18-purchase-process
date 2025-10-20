#!/bin/bash
echo "Waiting for Odoo to be ready..."
sleep 30

echo "Installing purchase_process module..."
docker-compose exec odoo odoo -i purchase_process --stop-after-init

echo "Module installation completed!"
