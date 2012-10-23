from django.core.management.base import BaseCommand
from api import events
from minecraft.models import Server

class Command(BaseCommand):
  help = 'Flush all events from the queue. Probably will break everything.'

  def handle(self, *args, **options):
    servers = Server.objects.all()
    for s in servers:
      queue = events.server_queue(s)
      stats = queue.stats()
      for t in queue.tubes():
        queue.use(t)
        job = queue.peek_ready()
        while job:
          print "Deleting %s from %s: %s"%(job.jid, t, job.body)
          job.delete()
          job = queue.peek_ready()
