#!/bin/bash

git -C /home/deploy/SecurityCiphers checkout master -f
git -C /home/deploy/SecurityCiphers pull origin
source /home/deploy/SecurityCiphers/venv/bin/activate
python /home/deploy/SecurityCiphers/ciphers/manage.py makemigrations
python /home/deploy/SecurityCiphers/ciphers/manage.py migrate
python /home/deploy/SecurityCiphers/ciphers/manage.py collectstatic --noinput
sudo /bin/systemctl restart ciphersite
echo "Landed $1 commits on $2 at $(date)" >> /home/deploy/webhook_log.txt