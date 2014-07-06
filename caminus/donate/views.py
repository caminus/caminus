from django.shortcuts import render_to_response
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from notification import models as notification
import urllib2
import json
import forms
import models
import signals
import stripe

def index(request):
    if request.method == 'POST':
        form = forms.DonationForm(request.POST, prefix='base')
        stripeForm = forms.StripeForm(request.POST, prefix='stripe')
    else:
        form = forms.DonationForm(prefix='base')
        stripeForm = forms.StripeForm(prefix='stripe')
    if form.is_valid():
        if int(form.cleaned_data['method']) == forms.DonationForm.METHOD_DWOLLA:
            data = {}
            order = {}
            item = {}
            item['Description'] = "Caminus Donation"
            item['Name'] = "Caminus Donation"
            item['Price'] = str(form.cleaned_data['quantity'])
            item['Quantity'] = 1
            order['OrderItems'] = [item,]
            order['Test'] = True
            order['Tax'] = 0.00
            order['Total'] = str(form.cleaned_data['quantity'])
            order['DestinationId'] = settings.DWOLLA_API_ID
            data['PurchaseOrder'] = order
            data['Key'] = settings.DWOLLA_API_KEY
            data['Secret'] = settings.DWOLLA_API_SECRET
            data['Callback'] = 'http://camin.us%s'%reverse('donate.views.dwollaCallback')
            donation = models.Donation.objects.create(quantity=form.cleaned_data['quantity'], user=request.user)
            order['OrderId'] = donation.id
            data['Redirect'] = 'http://camin.us%s'%reverse('donate.views.thanks', kwargs={'donation':donation.id})
            req = urllib2.Request("https://www.dwolla.com/payment/request", data=json.dumps(data), headers={'Content-Type': 'application/json'})
            response = json.load(urllib2.urlopen(req))
            return HttpResponseRedirect("https://www.dwolla.com/payment/checkout/%s"%(response['CheckoutId']))
        elif stripeForm.is_valid():
            stripe.api_key = settings.STRIPE_KEY
            cardData = {}
            cardData['number'] = stripeForm.cleaned_data['card']
            cardData['exp_month'] = stripeForm.cleaned_data['month']
            cardData['exp_year'] = stripeForm.cleaned_data['year']
            cardData['cvc'] = stripeForm.cleaned_data['cvc']
            try:
                charge = stripe.Charge.create(
                    amount = str(form.cleaned_data['quantity']*100),
                    currency = 'usd',
                    card = cardData,
                    description = 'Caminus Donation from %s'%(request.user.email)
                )
            except stripe.CardError, e:
                messages.error(request, "There was an error while processing your card: %s"%(e.message))
                return render_to_response('donate/index.html', {'form': form,
                  'stripeForm': stripeForm}, context_instance = RequestContext(request))
            donation = models.Donation.objects.create(quantity=form.cleaned_data['quantity'], user=request.user)
            donation.status = models.Donation.STATUS_PAID
            donation.transactionId = charge.id
            donation.save()
            acct = donation.user.minecraftprofile.currencyaccount
            acct.balance = F('balance')+(donation.quantity*2000)
            acct.save()
            notification.send_now([donation.user], "donation_paid", {"donation":donation, "credit":donation.quantity*2000})
            return HttpResponseRedirect('http://camin.us%s'%reverse('donate.views.thanks', kwargs={'donation':donation.id}))
    return render_to_response('donate/index.html', {'form': form,
      'stripeForm': stripeForm}, context_instance = RequestContext(request))

@csrf_exempt
def dwollaCallback(request):
    if request.method =='POST':
        data = json.loads(request.raw_post_data)
        donation = models.Donation.objects.get(id=data['OrderId'])
        donation.status = models.Donation.STATUS_PAID
        donation.transactionId = data['TransactionId']
        donation.save()
        acct = donation.user.minecraftprofile.currencyaccount
        acct.balance = F('balance')+(donation.quantity*2000)
        acct.save()
        notification.send_now([donation.user], "donation_paid", {"donation":donation, "credit":donation.quantity*2000})
    return HttpResponse(status=204)

def thanks(request, donation):
    donationObj = models.Donation.objects.get(id=donation)
    return render_to_response('donate/thanks.html', {'donation': donationObj}, context_instance = RequestContext(request))
