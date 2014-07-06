from django.utils import unittest
from django.test.client import Client
from django.contrib.auth.models import User
import json
import forms
import models

class DwollaTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('ValidUsername',
            'test@example.com', 'password')
        self.client.login(username='ValidUsername', password='password')

    def tearDown(self):
        self.user.delete()
        for d in models.Donation.objects.all():
            d.delete()

    def testStartDwolla(self):
        resp = self.client.post('/donate/', {
            'base-method': forms.DonationForm.METHOD_DWOLLA,
            'base-quantity': 100
        })
        self.assertEqual(resp.status_code, 302)
        donations = models.Donation.objects.all()
        self.assertEqual(len(donations), 1)
        self.assertEqual(donations[0].status, models.Donation.STATUS_PENDING)
        self.assertEqual(donations[0].quantity, 100)
        #FIXME: Test transactionId
    
    def testFinishDwolla(self):
        resp = self.client.post('/donate/', {
            'base-method': forms.DonationForm.METHOD_DWOLLA,
            'base-quantity': 200
        })
        self.assertEqual(resp.status_code, 302)
        donation = models.Donation.objects.all()[0]
        resp = self.client.post('/donate/dwolla', json.dumps({
            'OrderId': donation.id,
            'TransactionId': donation.transactionId
        }), 'text/json')
        donation = models.Donation.objects.all()[0]
        self.assertEqual(donation.status, models.Donation.STATUS_PAID)
        self.assertEqual(donation.quantity, 200)
        self.assertEqual(resp.status_code, 204)

class StripeTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('ValidUsername',
            'test@example.com', 'password')
        self.client.login(username='ValidUsername', password='password')

    def tearDown(self):
        self.user.delete()
        for d in models.Donation.objects.all():
            d.delete()

    def testValidCard(self):
        resp = self.client.post('/donate/', {
            'base-method': forms.DonationForm.METHOD_STRIPE,
            'base-quantity': 300,
            'stripe-card': '4242424242424242',
            'stripe-month': '12',
            'stripe-year': '2020',
            'stripe-cvc': '123',
        })
        print resp.content
        self.assertEqual(resp.status_code, 302)
        donations = models.Donation.objects.all()
        self.assertEqual(len(donations), 1)
        self.assertEqual(donations[0].status, models.Donation.STATUS_PAID)
        self.assertEqual(donations[0].quantity, 300)

    def testDeclinedCard(self):
        resp = self.client.post('/donate/', {
            'base-method': forms.DonationForm.METHOD_STRIPE,
            'base-quantity': 300,
            'stripe-card': '4000000000000002',
            'stripe-month': '12',
            'stripe-year': '2038',
            'stripe-cvc': '000',
        })
        self.assertEqual(resp.status_code, 200)
        donations = models.Donation.objects.all()
        self.assertEqual(len(donations), 0)

    def testBad(self):
        resp = self.client.post('/donate/', {
            'base-method': forms.DonationForm.METHOD_STRIPE,
            'base-quantity': 400,
            'stripe-card': '4242424242424242',
            'stripe-month': '12',
            'stripe-year': '2038',
            'stripe-cvc': '99',
        })
        self.assertEqual(resp.status_code, 200)
        donations = models.Donation.objects.all()
        self.assertEqual(len(donations), 0)

    def testBadCVC(self):
        resp = self.client.post('/donate/', {
            'base-method': forms.DonationForm.METHOD_STRIPE,
            'base-quantity': 400,
            'stripe-card': '4242424242424242',
            'stripe-month': '12',
            'stripe-year': '2038',
            'stripe-cvc': '99',
        })
        self.assertEqual(resp.status_code, 200)
        donations = models.Donation.objects.all()
        self.assertEqual(len(donations), 0)

    def testBadNumber(self):
        resp = self.client.post('/donate/', {
            'base-method': forms.DonationForm.METHOD_STRIPE,
            'base-quantity': 400,
            'stripe-card': '4242424242424241',
            'stripe-month': '12',
            'stripe-year': '2038',
            'stripe-cvc': '000',
        })
        self.assertEqual(resp.status_code, 200)
        donations = models.Donation.objects.all()
        self.assertEqual(len(donations), 0)
