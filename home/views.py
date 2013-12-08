#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#========================================================================
#   FileName: views.py
#     Author: ligen
#      Email: helios.ligen@gmail.com
#    Summary: 
# LastChange: 2013-11-28 14:42:36
#    History: 
#========================================================================

# Create your views here.

from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.generic.base import View

import models
import forms

def invoke(request, *args):
    args = [arg for arg in args if arg]
    view = eval(args[0])
    return view(request, *args[1:])

#@login_required

class GuaranteeView(View):

    def get(self, request, policy_id):
        return render(request, 'guarantee.html', dict(form = forms.GuaranteeForm(), policy_id = policy_id))

    def post(self, request, *args):
        form = forms.GuaranteeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            guarantor = models.Profile.objects.get(user = request.user)
            policy_id = request.POST['policy_id']
            policy = models.Policy.objects.get(id = int(policy_id))
            mortgage = models.Mortgage(guarantor=guarantor, quota = cd['quota'], policy = policy)
            mortgage.save()
            messages.info(request, "Guaranteed ￥%s successfully."%cd['quota'])
            return redirect(reverse('home'))

def home(request):
    policies = models.Policy.objects.all()
    return render(request, 'home.html', locals())

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            profile = models.Profile(user = new_user)
            profile.save()
            return HttpResponse("signed up !")
        else:
            #return HttpResponse("invalid input!")
            return HttpResponseRedirect(reverse('home'))
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', locals())

def release(request):
    if request.method == 'POST':
        form = forms.BitcoinHedge(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponse(cd['amount'])
        else:
            return HttpResponse("invalid")
    else:
        form = forms.BitcoinHedge()
    return render_to_response('sponse.html', dict(form = form),
            context_instance = RequestContext(request))

@login_required
def sponse(request):
    if request.method == 'POST':
        form = forms.IntentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            sponsor = models.Profile.objects.get(user=request.user)
            intent = models.Intent(sponsor = sponsor, cell = cd['cell'], words = cd['description'])
            intent.save()

            messages.info(request, "Thanks for your letter, we'll reply you ASAP. ")
            return redirect(reverse('home'))
        else:
            return HttpResponse("Oops, some input is invalid!")
            #messages.error(request, "Oops, some input is invalid!")
            #return render(request, "sponse.html")
    else:
        form = forms.IntentForm()
    return render_to_response('sponse.html', dict(form = form),
            context_instance = RequestContext(request))
