#!/bin/sh
if [ ! -f virtualenv/bin/activate ];then
  virtualenv --no-site-packages virtualenv/
fi
source virtualenv/bin/activate
pip install -r pip-requirements
coverage run ./manage.py test $@
ret=$?
if [ $ret -eq 0 ];then
    coverage report -m --include=\* --omit=\*/migrations/\*,settings.py,local_settings.py,manage.py
fi
exit $ret
