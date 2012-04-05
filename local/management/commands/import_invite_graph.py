from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.db import connections, connection
from local.models import Invite

class Command(BaseCommand):
    args = 'dbConfig'
    help = 'Synchronize from a drupal mysql database'

    def handle(self, *args, **options):
        if len(args) == 0:
            c = connection.cursor()
        else:
            c = connections[args[0]].cursor()
        c.execute("SELECT src.name AS inviter, dst.name AS invitee FROM users AS src LEFT JOIN invite ON invite.uid=src.uid LEFT JOIN users AS dst ON invite.invitee=dst.uid WHERE src.name IS NOT null AND dst.name IS NOT null")
        for link in c:
            if len(link[0]) == 0 or len(link[1]) == 0:
                continue
            try:
                sourceUser = User.objects.get(username__iexact=link[0])
            except ObjectDoesNotExist, e:
                print "Source user not found: %s"%(link[0])
                continue
            try:
                destUser = User.objects.get(username__iexact=link[1])
            except ObjectDoesNotExist, e:
                print "Destination user not found: %s"%(link[1])
                continue
            try:
                i = Invite.objects.get(creator=sourceUser, claimer=destUser)
            except ObjectDoesNotExist, e:
                Invite.objects.create(creator=sourceUser, claimer=destUser)
                print "Linked %s -> %s"%(sourceUser, destUser)
                continue
            print "Users already linked: %s -> %s"%(sourceUser, destUser)

