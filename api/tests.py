from django.utils import unittest
import json
from django.test.client import Client
from django.contrib.auth.models import User
from minecraft.models import MinecraftProfile

class MOTDTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def testUnregisteredUser(self):
        response = json.loads(self.client.get('/api/motd/NewUser').content)
        self.assertIsInstance(response['motd'], list)

class BalanceTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('ValidUsername', 'test@example.com')
        self.user.set_password('password')
        self.user.save()
        self.user.minecraftprofile.mc_username = "ValidUsername"
        self.user.minecraftprofile.save()
        self.user.minecraftprofile.currencyaccount.balance = 1000
        self.user.minecraftprofile.currencyaccount.save()

    def tearDown(self):
        self.user.delete()

    def testWithoutLogin(self):
        result = self.client.get('/api/balance').content
        self.assertEqual(result, "")

    def testWithLogin(self):
        self.client.login(username=self.user.username, password='password')
        response = json.loads(self.client.get('/api/balance').content)
        self.assertEqual(response['balance'], 1000)


class WhitelistTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('ValidUsername', 'test@example.com')
        self.user.minecraftprofile.mc_username = "ValidUsername"
        self.user.minecraftprofile.save()

    def tearDown(self):
        self.user.delete()

    def testValidProfile(self):
        response = json.loads(self.client.get('/api/validate/ValidUsername').content)
        self.assertEqual(response['valid'], True)

    def testInvalidProfile(self):
        response = json.loads(self.client.get('/api/validate/InvalidUser').content)
        self.assertEqual(response['valid'], False)

