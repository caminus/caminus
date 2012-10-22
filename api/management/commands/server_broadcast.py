from django.core.management.base import BaseCommand
from api import events
from minecraft.models import Server

class Command(BaseCommand):
  help = 'Send a broadcast event to all configured servers'

  def handle(self, *args, **options):
    servers = Server.objects.all()
    events.server_broadcast(' '.join(args))
    print "Event queued."
