from django.utils import unittest
from django.contrib.auth.models import User
from models import Badge, Award
import api

class APITest(unittest.TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@example.com')
        self.badge = Badge.objects.create(name="test", description="description", slug="test")
        self.awarded = False

    def tearDown(self):
        self.user.delete()
        self.badge.delete()
        api.badge_awarded.disconnect()

    def testCreateBadge(self):
        badge = api.create_badge("test_badge", "Test Badge", "Test Description")
        self.assertEqual(badge, api.find_badge("test_badge"))

    def testAward(self):
        api.award(self.user, "test", "reason")
        award = Award.objects.get(badge=self.badge, user=self.user)
        self.assertEqual(award.reason, "reason")
        self.assertEqual(award.badge, self.badge)
        self.assertTrue(api.user_has_badge(self.user, "test"))

    def _gotAward(self, sender, *args, **kwargs):
        self.awarded = True

    def testSignal(self):
        api.badge_awarded.connect(self._gotAward)
        api.award(self.user, "test", "reason")
        self.assertTrue(self.awarded)

    def testSingleSignal(self):
        api.create_badge("test_badge", "Test Badge", "Test Desc")
        api.badge_awarded.connect(self._gotAward, sender=api.find_badge("test_badge"))
        api.award(self.user, "test_badge", "reason")
        self.assertTrue(self.awarded)
