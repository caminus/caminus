from django.shortcuts import render_to_response
from django.conf import settings
from django.core.urlresolvers import reverse
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

def index(request):
    if request.method == 'POST':
        form = forms.DonationForm(request.POST)
    else:
        form = forms.DonationForm()
    if form.is_valid():
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
        data['Redirect'] = 'http://camin.us%s'%reverse('donate.views.thanks')
        donation = models.Donation.objects.create(quantity=form.cleaned_data['quantity'], user=request.user)
        order['OrderId'] = donation.id
        req = urllib2.Request("https://www.dwolla.com/payment/request", data=json.dumps(data), headers={'Content-Type': 'application/json'})
        response = json.load(urllib2.urlopen(req))
        return HttpResponseRedirect("https://www.dwolla.com/payment/checkout/%s"%(response['CheckoutId']))
    else:
        return render_to_response('donate/index.html', {'form': form}, context_instance = RequestContext(request))

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

def thanks(request):
    return render_to_response('donate/thanks.html')
