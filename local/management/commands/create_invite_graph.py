from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.db import connections, connection
from local.models import Invite

class Command(BaseCommand):
    help = 'Generate a dot graph of invited users'

    def handle(self, *args, **options):
        print "digraph G {"
        print "rankdir=\"LR\""
        for i in Invite.objects.all():
            if i.claimer is None:
                continue
            if i.creator is None:
                continue
            print "\"%s\" -> \"%s\""%(i.creator.__unicode__(), i.claimer.__unicode__())
        print "}"
