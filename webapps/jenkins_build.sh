#!/bin/bash
. /home/ubuntu/duelink-ci/bin/activate
cd /home/ubuntu/duelink-ci/duelink-build/webapps
pip install -r /home/ubuntu/duelink-ci/requirements.txt
python manage.py migrate
python manage.py test --reverse