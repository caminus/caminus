from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from django.core.urlresolvers import reverse
import models

class InviteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('ValidUsername', 'test@example.com')
        self.user.save()
        self.invite = models.Invite()
        self.invite.creator = self.user
        self.invite.save()

    def tearDown(self):
        self.invite.delete()
        self.user.delete()

    def testTryBadInvite(self):
        resp = self.client.get(reverse('local.views.claimInvite', kwargs={'code':self.invite.code+"-invalid"}), follow=True)
        self.assertEqual(404, resp.status_code)

    def testTryToReuseInvite(self):
        self.invite.claimer = self.user
        self.invite.save()
        resp = self.client.get(reverse('local.views.claimInvite', kwargs={'code':self.invite.code}), follow=True)
        self.assertEqual(404, resp.status_code)

    def testTryToUseDeletedInvite(self):
        self.invite.deleted = True
        self.invite.save()
        resp = self.client.get(reverse('local.views.claimInvite', kwargs={'code':self.invite.code}), follow=True)
        self.assertEqual(404, resp.status_code)

    def testUseInvite(self):
        resp = self.client.get(reverse('local.views.claimInvite', kwargs={'code':self.invite.code}), follow=True)
        self.assertEqual(200, resp.status_code)

class AccountCreationTest(TestCase):
    def testCreation(self):
        user = User.objects.create_user('ValidUser', 'test@example.com')
        self.assertIsNotNone(user.minecraftprofile.currencyaccount)
        user.delete()
