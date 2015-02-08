FROM ansible/centos7-ansible:stable

MAINTAINER Team Caminus <team@camin.us>

ADD . /srv/infrastructure
RUN ansible-playbook /srv/infrastructure/playbooks/www-config.yml | tee /srv/infrastructure/build.log

EXPOSE 3000
ENTRYPOINT ["uwsgi", "--ini", "/etc/uwsgi.ini"]
