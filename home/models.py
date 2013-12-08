from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Hedge(models.Model):
    sum = models.IntegerField() 
    fee = models.IntegerField()
    kickoff = models.DateField()
    deadline = models.DateField()

class Intent(models.Model):
    sponsor = models.ForeignKey('Profile')
    cell =  models.CharField(max_length=15)
    words = models.TextField()

    def __unicode__(self):
        return self.words

class Policy(models.Model):
    sponsor = models.ForeignKey('Profile')
    title = models.CharField(max_length=50)
    catagory = models.CharField(max_length=10)
    funded = models.IntegerField(default = 0)
    sum = models.IntegerField() 
    grade = models.IntegerField()
    reward = models.FloatField()
    kickoff = models.DateField()
    deadline = models.DateField()

    def __unicode__(self):
        return self.title

class Profile(models.Model):
    balance = models.IntegerField(default = 0)
    user = models.ForeignKey(User)
    mortgages = models.ManyToManyField(Policy, through = 'Mortgage')

    def __unicode__(self):
        return self.user.username

    def recharge(self, money):
        self.balance += money
        self.save()
        return money

    def charge(self, money):
        if self.balance < 0:
            return -1
        else:
            self.balance -= money
            self.save()
            return money

class Mortgage(models.Model):
    guarantor = models.ForeignKey(Profile)
    policy = models.ForeignKey(Policy)
    quota = models.IntegerField()

    def save(self):
        self.policy.funded += self.quota
        self.policy.save()
        super(Mortgage, self).save()
