#!/bin/bash

cd /home/deploy/SecurityCiphers
git checkout master && git pull -f
source /home/deploy/SecurityCiphers/venv/bin/activate
python /home/deploy/SecurityCiphers/ciphers/manage.py makemigrations
python /home/deploy/SecurityCiphers/ciphers/manage.py migrate
python /home/deploy/SecurityCiphers/ciphers/manage.py collectstatic --noinput
sudo /bin/systemctl restart ciphersite
echo "Completed GitHub Webhook Script at $(date)" >> /home/deploy/webhook_log.txt