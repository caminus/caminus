from django.db.models.signals import post_syncdb
import badges.api
import badges.models
from django.contrib.auth.models import User

def create_playtime_badges(app, created_models, verbosity, **kwargs):
    badges.api.create_badge("24h_playtime", "24 Hours of Playtime", "You've played a combined total of 24 hours")
    badges.api.create_badge("7d_playtime", "7 Days of Playtime", "You've played a combined total of 7 days")
    badges.api.create_badge("30d_playtime", "30 Days of Playtime", "You've played a combined total of 30 days")

post_syncdb.connect(create_playtime_badges, sender=badges.models)
