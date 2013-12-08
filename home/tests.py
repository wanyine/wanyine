"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from datetime import date, timedelta

from django.test import TestCase
from django.http import HttpRequest
import models
import views
import ajax

class IntegrationTest(TestCase):
    def test_home(self):
        self.assertTrue(self.client.get(''))

    def test_guarantee(self):
        response = self.client.get('/guarantee/1/')
        self.assertTrue(response.content)
        self.assertEqual('', response.content)

    def test_sponse(self):
        response = self.client.post('/sponse/')
        self.assertTrue(response)
        #self.assertEqual("123", response.content)

    def test_release(self):
        response = self.client.get('/release/')
        #self.assertEqual("", response.content)
        response = self.client.post('/release/',dict(amount=123, fee="12"))
        self.assertEqual("123", response.content)

class ModelsTest(TestCase):

    def create_profile(self, username = 'test', balance = 0):
        user = models.User.objects.create_user(username)
        profile = models.Profile(user = user, balance = balance)
        profile.save()
        return profile

    def create_policy(self, sponsor, kickoff = date.today()):
        policy = models.Policy(
                sponsor = sponsor,
                sum = 10000,
                kickoff= kickoff,
                deadline = kickoff + timedelta(days = 365),
                reward = 3,
                grade = 1,
                catagory = 'Health',
                title = 'protect your hands'
                )
        policy.save()
        return policy 

    def test_profile(self):
        profile = self.create_profile()
        self.assertEqual('test', profile.user.username)
        self.assertEqual(1, profile.id)

    def test_policy(self):
        profile = self.create_profile()
        policy = self.create_policy(profile)
        self.assertEqual(1, policy.id)
        self.assertEqual(policy, models.Policy.objects.all().get())

    def test_mortgage(self):
        sponsor = self.create_profile()
        policy = self.create_policy(sponsor)
        guarantor = self.create_profile('another', 100)
        self.assertFalse(guarantor.mortgages.all())
        mort = models.Mortgage(policy = policy, guarantor = guarantor, quota = 90)
        mort.save()
        saved = models.Policy.objects.get()
        self.assertEqual(policy, saved)
        self.assertTrue(guarantor.mortgages.all())
        self.assertEqual(policy, guarantor.mortgages.all().get())
        self.assertEqual(90, saved.funded)

class ViewsTest(TestCase):

    def test_sponse(self):
        request = HttpRequest() 
        request.user = models.User.objects.create_user('test')
        response = views.sponse(request)
        self.assertTrue(response)

class AjaxTest(TestCase):
    def test_sayHello(self):
        response = ajax.sayHello(HttpRequest())
        self.assertTrue(response)

    def test_guarantee(self):
        pass
