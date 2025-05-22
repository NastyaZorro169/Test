#!/bin/bash
set -e

echo "Applying database migrations..."
python manage.py migrate
python manage.py shell -c "from core.management.commands.generate_test_data import Command; Command().handle()"


echo "Starting server..."
exec "$@"
