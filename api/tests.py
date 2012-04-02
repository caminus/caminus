from django.utils import unittest
import json
from django.test.client import Client
from django.contrib.auth.models import User
from minecraft.models import MinecraftProfile, Server, PlayerSession
import hashlib

class ServerPingTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('ValidUsername', 'test@example.com')
        self.user.minecraftprofile.mc_username = "ValidUsername"
        self.user.minecraftprofile.save()
        self.server = Server.objects.create(hostname='localhost', secret='secret')
        tokenHash = hashlib.sha1()
        tokenHash.update("%s%s%s"%('localhost', 0, 'secret'))
        self.token = "%s$%s$%s"%('localhost', 0, tokenHash.hexdigest())

    def tearDown(self):
        self.user.delete()
        self.server.delete()

    def testPing(self):
        resp = self.client.get('/api/server/whoami', HTTP_AUTHORIZATION='X-Caminus %s'%(self.token))
        self.assertEqual(resp.status_code, 200)

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

class SessionTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('ValidUsername', 'test@example.com')
        self.user.minecraftprofile.mc_username = "ValidUsername"
        self.user.minecraftprofile.save()
        self.server = Server.objects.create(hostname='localhost', secret='secret')
        tokenHash = hashlib.sha1()
        tokenHash.update("%s%s%s"%('localhost', 0, 'secret'))
        self.token = "%s$%s$%s"%('localhost', 0, tokenHash.hexdigest())

    def tearDown(self):
        self.user.delete()
        self.server.delete()

    def testSessionStart(self):
        resp = self.client.post('/api/server/session/%s'%(self.user.minecraftprofile.mc_username), {'hostname':self.server.hostname, 'ip': '127.0.0.1'}, HTTP_AUTHORIZATION="X-Caminus %s"%(self.token))
        self.assertEqual(resp.status_code, 200)
        session = json.loads(resp.content)
        sessionObj = PlayerSession.objects.get(id__exact=session['session'])

    def testSessionEnd(self):
        resp = self.client.post('/api/server/session/%s'%(self.user.minecraftprofile.mc_username), {'hostname':self.server.hostname, 'ip': '127.0.0.1'}, HTTP_AUTHORIZATION="X-Caminus %s"%(self.token))
        session = json.loads(resp.content)
        resp = self.client.put('/api/server/session/%s'%(self.user.minecraftprofile.mc_username), {'session':session['session']}, HTTP_AUTHORIZATION="X-Caminus %s"%(self.token))
        self.assertEqual(resp.status_code, 200)
        sessionObj = PlayerSession.objects.get(id__exact=session['session'])
        self.assertNotEqual(sessionObj.end, None)

class EconomyTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('ValidUsername', 'test@example.com')
        self.user.minecraftprofile.mc_username = "ValidUsername"
        self.user.minecraftprofile.save()
        self.user.minecraftprofile.currencyaccount.balance=42
        self.user.minecraftprofile.currencyaccount.save()
        self.server = Server.objects.create(hostname='localhost', secret='secret')
        tokenHash = hashlib.sha1()
        tokenHash.update("%s%s%s"%('localhost', 0, 'secret'))
        self.token = "%s$%s$%s"%('localhost', 0, tokenHash.hexdigest())

    def tearDown(self):
        self.user.delete()
        self.server.delete()

    def testBalanceQuery(self):
        resp = self.client.get('/api/server/economy/ValidUsername', HTTP_AUTHORIZATION="X-Caminus %s"%(self.token))
        data = json.loads(resp.content)
        self.assertEqual(data['balance'], 42)

    def testDeposit(self):
        resp = self.client.put('/api/server/economy/ValidUsername', {'delta': 100}, HTTP_AUTHORIZATION="X-Caminus %s"%(self.token))
        data = json.loads(resp.content)
        self.assertEqual(data['balance'], 142)

    def testWithdraw(self):
        resp = self.client.put('/api/server/economy/ValidUsername', {'delta': -40}, HTTP_AUTHORIZATION="X-Caminus %s"%(self.token))
        data = json.loads(resp.content)
        self.assertEqual(data['balance'], 2)
