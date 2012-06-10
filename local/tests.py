from django.test import TestCase
from django.db.models.signals import post_syncdb
from django.contrib.auth.models import User
from django.test.client import Client
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core import mail
import context
import badges.api
import models
from donate.models import Donation
from django.http import HttpRequest

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

    def testInviteURL(self):
        resp = self.client.get(self.invite.get_absolute_url())
        self.assertEqual(self.client.session['profile-invite'], self.invite)

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

class RewardTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('User', 'test@example.com')
        self.badge = badges.api.create_badge("api_test", "API Test", "test")
        self.reward = models.AwardBonus.objects.create(badge=self.badge, value=1000)

    def tearDown(self):
        self.user.delete()
        self.badge.delete()
        self.reward.delete()

    def testReward(self):
        account = self.user.minecraftprofile.currencyaccount
        preValue = account.balance
        badges.api.award(self.user, "api_test")
        account = models.CurrencyAccount.objects.get(pk=account.pk)
        self.assertEqual(account.balance-preValue, self.reward.value)

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

class QuoteContextTest(TestCase):
    def testEmptyQuotes(self):
        ret = context.random_quote(HttpRequest())
        self.assertFalse('quote' in ret)

    def testSingleQuote(self):
        q = models.Quote.objects.create(text="test")
        ret = context.random_quote(HttpRequest())
        self.assertTrue(ret['quote'].text == unicode(ret['quote']))
        q.delete()

    def testRandomQuote(self):
        q = models.Quote.objects.create(text="text")
        q1 = models.Quote.objects.create(text="text2")
        ret = context.random_quote(HttpRequest())
        self.assertTrue('quote' in ret)
        q.delete()
        q1.delete()

class DonationContextTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@example.com')
        self.donation = None

    def tearDown(self):
        self.user.delete()
        if self.donation:
            self.donation.delete()

    def testNoGoal(self):
        delattr(settings, 'CAMINUS_DONATION_GOAL')
        ret = context.donation_info(HttpRequest())
        self.assertTrue(ret['donation_goal_progress'] == 100)
        self.assertTrue(ret['donation_month_total'] == 0)
        self.assertTrue(ret['donation_month_goal'] == 0)

    def testNoProgress(self):
        settings.CAMINUS_DONATION_GOAL = 100
        ret = context.donation_info(HttpRequest())
        self.assertTrue(ret['donation_goal_progress'] == 0)
        self.assertTrue(ret['donation_month_total'] == 0)
        self.assertTrue(ret['donation_month_goal'] == 100)

    def testOverachieved(self):
        settings.CAMINUS_DONATION_GOAL = 100
        self.donation = Donation.objects.create(quantity=300, user=self.user, status=Donation.STATUS_PAID)
        ret = context.donation_info(HttpRequest())
        self.assertTrue(ret['donation_goal_progress'] == 100)
        self.assertTrue(ret['donation_month_total'] == 300)
        self.assertTrue(ret['donation_month_goal'] == 100)

    def testAchieved(self):
        settings.CAMINUS_DONATION_GOAL = 100
        self.donation = Donation.objects.create(quantity=100, user=self.user, status=Donation.STATUS_PAID)
        ret = context.donation_info(HttpRequest())
        self.assertTrue(ret['donation_goal_progress'] == 100)
        self.assertTrue(ret['donation_month_total'] == 100)
        self.assertTrue(ret['donation_month_goal'] == 100)

    def testPartiallyAchieved(self):
        settings.CAMINUS_DONATION_GOAL = 100
        self.donation = Donation.objects.create(quantity=50, user=self.user, status=Donation.STATUS_PAID)
        ret = context.donation_info(HttpRequest())
        self.assertTrue(ret['donation_goal_progress'] == 50)
        self.assertTrue(ret['donation_month_total'] == 50)
        self.assertTrue(ret['donation_month_goal'] == 100)
