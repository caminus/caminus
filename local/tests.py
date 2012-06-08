from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.core import mail
import badges.api
import models

class InviteUseTest(TestCase):
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

    def testRegisterViaInvite(self):
        resp = self.client.get(reverse('local.views.claimInvite', kwargs={'code':self.invite.code}), follow=True)
        self.assertEqual(200, resp.status_code)
        data = {}
        data['user-username'] = 'TestUser'
        data['user-password'] = 'abcd'
        data['user-password_confirm'] = 'abcd'
        data['user-email'] = 'email@example.com'
        data['profile-mc_username'] = 'Testificate'
        resp = self.client.post(reverse('local.views.register' ), data)
        self.assertEqual(len(mail.outbox), 1)

class InviteManageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('ValidUsername', 'test@example.com', 'password')
        self.user.save()
        self.client.login(username='ValidUsername', password='password')

    def tearDown(self):
        self.user.delete()

    def testCreateMaxInvites(self):
        for i in range(0, 100):
            self.client.get(reverse('local.views.createInvite'))
        self.assertEqual(len(self.user.invites.all()), 2)

    def testDeleteInvites(self):
        self.client.get(reverse('local.views.createInvite'))
        self.client.post(reverse('local.views.deleteInvite', kwargs={'code':self.user.invites.all()[0]}))
        self.assertEqual(len(self.user.invites.exclude(deleted=True)), 0)

class AccountCreationTest(TestCase):
    def testCreation(self):
        user = User.objects.create_user('ValidUser', 'test@example.com')
        self.assertIsNotNone(user.minecraftprofile.currencyaccount)
        user.delete()

class InviteBadgeTest(TestCase):
    def setUp(self):
        self.inviter = User.objects.create_user('Inviter', 'test@example.com')
        self.users = []

    def tearDown(self):
        self.inviter.delete()
        for u in self.users:
            u.delete()

    def testThree(self):
        self.assertFalse(badges.api.user_has_badge(self.inviter, "three_invites"))
        for i in range(0, 3):
            u = User.objects.create_user(i, 'test@example.com')
            self.users.append(u)
            models.Invite.objects.create(creator=self.inviter, claimer=u)
        self.assertTrue(badges.api.user_has_badge(self.inviter, "three_invites"))

    def testMultipleThree(self):
        self.assertFalse(badges.api.user_has_badge(self.inviter, "three_invites"))
        for i in range(0, 3):
            u = User.objects.create_user(i, 'test@example.com')
            self.users.append(u)
            models.Invite.objects.create(creator=self.inviter, claimer=u)
        self.assertTrue(badges.api.user_has_badge(self.inviter, "three_invites"))
        self.assertEqual(1, len(self.inviter.awards.filter(badge__pk=badges.api.find_badge("three_invites").pk)))
