#!/bin/sh
if [ ! -f virtualenv/bin/activate ];then
  virtualenv --no-site-packages virtualenv/
fi
source virtualenv/bin/activate
pip install -r pip-requirements
exec ./manage.py test $@
