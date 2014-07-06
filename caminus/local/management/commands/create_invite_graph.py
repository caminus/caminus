from django.core.management.base import BaseCommand
from local import social_graph

class Command(BaseCommand):
    help = 'Generate a dot graph of invited users'

    def handle(self, *args, **options):
        g = social_graph()
        print g.create_dot()
