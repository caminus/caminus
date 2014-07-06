import django.dispatch

donation_paid = django.dispatch.Signal(providing_args=["donation"])
