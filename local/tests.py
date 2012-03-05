from django.test import TestCase
from django.contrib.auth.models import User


class AccountCreationTest(TestCase):
    def testCreation(self):
        user = User.objects.create_user('ValidUser', 'test@example.com')
        self.assertIsNotNone(user.minecraftprofile.currencyaccount)
        user.delete()
