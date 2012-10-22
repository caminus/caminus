from django.core.management.base import BaseCommand
from api import events
from minecraft.models import Server

class Command(BaseCommand):
  help = 'Display statistics about the event queue'

  def handle(self, *args, **options):
    servers = Server.objects.all()
    for s in servers:
      queue = events.server_queue(s)
      stats = queue.stats()
      print s
      for k,v in stats.iteritems():
        print "\t%s: %s"%(k, v)
      print "\tTubes:"
      for t in queue.tubes():
        print "\t\t%s"%(t)
      next = queue.peek_ready()
      if next:
        print "\tNext job: %s"%(next.body)
      else:
        print "\tNo pending job."
