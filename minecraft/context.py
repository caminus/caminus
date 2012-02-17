import models

def random_quote(request):
    quote = models.Quote.objects.order_by('?')[0]
    return {'quote': quote}
