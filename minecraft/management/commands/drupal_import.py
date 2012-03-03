from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.db import connections, connection

class Command(BaseCommand):
    args = 'dbConfig'
    help = 'Import from a drupal mysql database'

    def handle(self, *args, **options):
        try:
    	    importGroup = Group.objects.get(name__exact='Imported Users')
	except ObjectDoesNotExist, e:
	    importGroup = Group()
	    importGroup.name = 'Imported Users'
	    importGroup.save()
	if len(args) == 0:
	    c = connection.cursor()
	else:
	    c = connections[args[0]].cursor()
	c.execute("SELECT name, pass, mail, picture, created, access, username FROM `users` LEFT JOIN `minecraft_users` ON `users`.uid = `minecraft_users`.`uid`");
    	for u in c:
	    if u[6] is None or len(u[0]) == 0:
	        continue
	    try:
	        djangoUser = User.objects.get(username__exact=u[0])
		print "Skipping already imported user %s"%(u[0])
		continue
 	    except ObjectDoesNotExist, e:
	        djangoUser = User()
	    djangoUser.username = u[0]
	    djangoUser.password = 'md5$$'+u[1]
	    djangoUser.email = u[2]
	    djangoUser.date_joined = datetime.fromtimestamp(u[4])
	    djangoUser.last_login = datetime.fromtimestamp(u[4])
	    djangoUser.save()
	    djangoUser.groups.add(importGroup)
	    djangoUser.save()
	    profile = djangoUser.get_profile()
	    profile.mc_username = u[6]
	    profile.save()
	    print "Imported %s <%s>"%(u[0], u[6])
