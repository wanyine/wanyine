from django import forms
from django.contrib.localflavor.cn.forms import CNCellNumberField

class Hedge(forms.Form):
    category = forms.ChoiceField()

class BitcoinHedge(forms.Form):
    amount = forms.IntegerField()
    #kickoff = forms.DateField()
    #lifetime = forms.ChoiceField()
    fee = forms.IntegerField()

class IntentForm(forms.Form):
    cell = CNCellNumberField()
    description = forms.CharField(widget = forms.Textarea)
    #description = forms.FileField()

class GuaranteeForm(forms.Form):
    quota = forms.IntegerField()
