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
        queue.watch(t)
      job = queue.reserve(0)
      while job:
        print "Deleting %s: %s"%(job.jid, job.body)
        job.delete()
        job = queue.reserve(0)
