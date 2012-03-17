from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.db import connections, connection
from local.models import CurrencyAccount

class Command(BaseCommand):
    args = 'dbConfig'
    help = 'Synchronize from a drupal mysql database'

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
        c.execute("SELECT name, pass, mail, picture, created, access, username, SUM(`txn`.value) FROM `users` LEFT JOIN `minecraft_users` ON `users`.uid = `minecraft_users`.`uid` LEFT JOIN `virtual_currency_txn` AS txn ON `txn`.uid=`users`.uid GROUP BY `users`.uid");
        for u in c:
            if u[6] is None or len(u[0]) == 0:
                continue
            try:
                djangoUser = User.objects.get(username__exact=u[0])
            except ObjectDoesNotExist, e:
                djangoUser = User.objects.create_user(u[0], u[2])
                djangoUser.date_joined = datetime.fromtimestamp(u[4])
                djangoUser.groups.add(importGroup)
            djangoUser.last_login = datetime.fromtimestamp(u[4])
            djangoUser.password = 'md5$$'+u[1]
            djangoUser.email = u[2]
            djangoUser.save()
            profile = djangoUser.minecraftprofile
            profile.mc_username = u[6]
            profile.save()
            if u[7]:
                try:
                    acct = profile.currencyaccount
                except ObjectDoesNotExist, e:
                    print "Missing currency account for %s. Fixing..."%(djangoUser)
                    acct = CurrencyAccount.objects.create(profile=profile)
                acct.balance = u[7]
                acct.save()
            print "Synchronized %s <%s>"%(u[0], u[6])
