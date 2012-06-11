from django.utils import unittest
import json
from django.test.client import Client
from django.contrib.auth.models import User
from minecraft.models import MinecraftProfile, Server, PlayerSession, MOTD, Ban
from local.models import Quote
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
        self.server = Server.objects.create(hostname="localhost", secret="")

    def tearDown(self):
        self.server.delete()

    def testUnregisteredUser(self):
        response = json.loads(self.client.get('/api/motd/NewUser').content)
        self.assertIsInstance(response['motd'], list)

    def testRandomMOTD(self):
        m = MOTD.objects.create(server=self.server, text="testMOTD")
        q = Quote.objects.create(text="testQUOTE")
        response = json.loads(self.client.get('/api/motd/NewUser').content)
        m.delete()
        q.delete()
        foundMOTD = False
        foundQuote = False
        for line in response['motd']:
            if line == "testMOTD":
                foundMOTD = True
            if line == '"testQUOTE"':
                foundQuote = True
        self.assertTrue(foundMOTD)
        self.assertTrue(foundQuote)

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

    def testBannedStart(self):
        b = Ban.objects.create(player=self.user.minecraftprofile, banner=self.user, reason="test")
        resp = self.client.post('/api/server/session/%s/new'%(self.user.minecraftprofile.mc_username), {'ip': '127.0.0.1'}, HTTP_AUTHORIZATION="X-Caminus %s"%(self.token))
        b.delete()
        self.assertEqual(resp.status_code, 200)
        session = json.loads(resp.content)
        self.assertFalse(session['valid'])

    def testBadUserStart(self):
        resp = self.client.post('/api/server/session/SomeUnknownUser/new', {'ip': '127.0.0.1'}, HTTP_AUTHORIZATION="X-Caminus %s"%(self.token))
        self.assertEqual(resp.status_code, 200)
        session = json.loads(resp.content)
        self.assertFalse(session['valid'])

    def testInactiveStart(self):
        self.user.is_active = False
        self.user.save()
        resp = self.client.post('/api/server/session/%s/new'%(self.user.minecraftprofile.mc_username), {'ip': '127.0.0.1'}, HTTP_AUTHORIZATION="X-Caminus %s"%(self.token))
        self.user.is_active = True
        self.user.save()
        self.assertEqual(resp.status_code, 200)
        session = json.loads(resp.content)
        self.assertFalse(session['valid'])

    def testSessionStart(self):
        resp = self.client.post('/api/server/session/%s/new'%(self.user.minecraftprofile.mc_username), {'ip': '127.0.0.1'}, HTTP_AUTHORIZATION="X-Caminus %s"%(self.token))
        self.assertEqual(resp.status_code, 200)
        session = json.loads(resp.content)
        print repr(session)
        self.assertTrue(session['valid'])

    def testSessionEnd(self):
        resp = self.client.post('/api/server/session/%s/new'%(self.user.minecraftprofile.mc_username), {'ip': '127.0.0.1'}, HTTP_AUTHORIZATION="X-Caminus %s"%(self.token))
        session = json.loads(resp.content)
        resp = self.client.get('/api/server/session/%s/close'%(self.user.minecraftprofile.mc_username), HTTP_AUTHORIZATION="X-Caminus %s"%(self.token))
        self.assertEqual(resp.status_code, 200)

class PollTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def testAnonymousPoll(self):
        resp = self.client.get('/api/poll/0')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue('server-info' in data)
        self.assertTrue('user-info' in data)
        self.assertEqual(len(data['user-info']), 0)

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
        self.assertTrue(data['success'])

    def testWithdraw(self):
        resp = self.client.put('/api/server/economy/ValidUsername', {'delta': -40}, HTTP_AUTHORIZATION="X-Caminus %s"%(self.token))
        data = json.loads(resp.content)
        self.assertEqual(data['balance'], 2)
        self.assertTrue(data['success'])

    def testOverdraw(self):
        resp = self.client.put('/api/server/economy/ValidUsername', {'delta': -400}, HTTP_AUTHORIZATION="X-Caminus %s"%(self.token))
        data = json.loads(resp.content)
        self.assertFalse(data['success'])
