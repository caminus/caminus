from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.core import mail
import badges.api
import models
from datetime import datetime,timedelta

class BadgeTest(TestCase):
    def setUp(self):
        self.player = User.objects.create_user('Player', 'test@example.com')
        self.server = models.Server.objects.create(hostname="localhost", secret="")

    def tearDown(self):
        self.player.delete()
        self.server.delete()

    def testOpenSession(self):
        self.assertFalse(badges.api.user_has_badge(self.player, "24h_playtime"))
        models.PlayerSession.objects.create(ip="127.0.0.1", start=datetime.now(), server=self.server, player=self.player.minecraftprofile)
        self.assertFalse(badges.api.user_has_badge(self.player, "24h_playtime"))

    def test24H(self):
        self.assertFalse(badges.api.user_has_badge(self.player, "24h_playtime"))
        now = datetime.now()
        models.PlayerSession.objects.create(ip="127.0.0.1", start=now, end=now+timedelta(days=2), server=self.server, player=self.player.minecraftprofile)
        self.assertTrue(badges.api.user_has_badge(self.player, "24h_playtime"))
