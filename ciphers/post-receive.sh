#!/bin/bash
echo "Pulling from master"
git -C /home/deploy/SecurityCiphers checkout master -f
git -C /home/deploy/SecurityCiphers pull origin
echo "Activating VENV"
source /home/deploy/SecurityCiphers/venv/bin/activate
echo "Installing new requirements"
pip3 install -r /home/deploy/SecurityCiphers/requirements.txt
echo "Migrating DB"
python /home/deploy/SecurityCiphers/ciphers/manage.py makemigrations
python /home/deploy/SecurityCiphers/ciphers/manage.py migrate
echo "Collecting static files"
python /home/deploy/SecurityCiphers/ciphers/manage.py collectstatic --noinput

echo "Restarting site uWSGI"
sudo /bin/systemctl restart ciphersite
echo "Landed $1 commits on $2 at $(date)" >> /home/deploy/webhook_log.txt