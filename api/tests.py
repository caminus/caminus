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
        resp = self.client.post('/api/server/session/%s/new'%(self.user.minecraftprofile.mc_username), {'ip': '127.0.0.1'}, HTTP_AUTHORIZATION="X-Caminus %s"%(self.token))
        self.assertEqual(resp.status_code, 200)
        session = json.loads(resp.content)

    def testSessionEnd(self):
        resp = self.client.post('/api/server/session/%s/new'%(self.user.minecraftprofile.mc_username), {'ip': '127.0.0.1'}, HTTP_AUTHORIZATION="X-Caminus %s"%(self.token))
        session = json.loads(resp.content)
        resp = self.client.get('/api/server/session/%s/close'%(self.user.minecraftprofile.mc_username), HTTP_AUTHORIZATION="X-Caminus %s"%(self.token))
        self.assertEqual(resp.status_code, 200)

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
