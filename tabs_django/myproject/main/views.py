# Create your views here.

import random

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.core.mail import send_mail

from django.http import HttpResponse

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from main.models import Registration, Search

def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))
    
def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))

def contact(request):
    return render_to_response('contact.html', context_instance=RequestContext(request))

def privacy(request):
    return render_to_response('privacy.html', context_instance=RequestContext(request))

def stats(request):
    toret = ''
    regs = Registration.objects.all()
    searches = Search.objects.all()
    toret += "Number of registrations: %d<br />\n" % len(regs)
    toret += "Number of activated registrations: %d<br />\n" % len(filter(lambda x: x.activated, regs))
    toret += "Number of unique registered citizens: %d<br /><br />\n" % len(set([reg.email for reg in regs]))
    toret += "Number of searches: %d<br />\n" % len(searches)
    toret += "Total number of searches: %d" % sum([srch.frequency for srch in searches])
    return HttpResponse(toret)

def misc_csv(request):
    import csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="keyword-stats.csv"'
    writer = csv.writer(response)
    data = Registration.objects.values()
    keys = list(data[0].keys())
    writer.writerows([keys] + [[obj[key] for key in keys] for obj in data])
    return response

def keywordcsv(request):
    import csv
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="keyword-stats.csv"'

    writer = csv.writer(response)
    
    for (key,val) in get_keyword_data().items():
        if key != '':
            writer.writerow([key, val])
    
    return response

def keyworddump(request):
    text = ''
    for (key,val) in get_keyword_data().items():
        if val > 1 and key != '':
            text += "%s:%d\n" % (key, val)
    return HttpResponse(text)
            
def get_keyword_data():
    freqs = {}
    words = []
    all_searches = Search.objects.all()
    for search in all_searches:
        words.extend(search.word_or_phrase.lower().replace('"','').split(' '))
    
    for kw in words:
        if kw not in freqs:
            freqs[kw] = 0
        freqs[kw] += 1
    
    return freqs

def subscribe(request, key):
    reg = Registration.objects.get(activation_key=key)
    reg.activated = True
    reg.save()
    return render_to_response('index.html', {'message': 'Email confirmed!'}, context_instance=RequestContext(request))

def unsubscribe(request, key):
    reg = Registration.objects.get(activation_key=key)
    reg.delete()
    return render_to_response('index.html', {'message': 'You have been unsubscribed.'}, context_instance=RequestContext(request))

def register(request):
    if request.method == 'POST':
        
        
        try:
            validate_email( request.POST['email'] )
        except ValidationError:
            return render_to_response('index.html', {'message': 'Invalid email provided.'}, context_instance=RequestContext(request))
    
        activation_val = "%010x" % random.getrandbits(42)
        
        reg = Registration(email = request.POST['email'],
                           activation_key = activation_val,
                           search_id = Search.objects.get(id=int(request.POST['search_id'])))
        reg.save()
        
        message = "Hello,\n  Thank you for signing up for a TABS Toronto search query."
        message += " Please go to the following url to confirm your email address:\n- "
        message += "http://www.tabstoronto.com/subscribe/%s/" % activation_val
        send_mail('[tabsto] Please register your email', message, 'notifications@tabstoronto.com',
                  [request.POST['email']], fail_silently=False)
    
    return index(request)
    

def search(request):
    if request.method != 'GET':
        return index(request)
    
    try:
        if 'search_id' in request.GET:
            search = Search.objects.get(id=int(request.GET['search_id']))
        else:
            search = Search.objects.get(word_or_phrase=request.GET['query'],
                                        committee=request.GET['decisionBodyId'],
                                        from_date=request.GET['fromDate'],
                                        to_date=request.GET['toDate'],
                                        item_status=request.GET['itemStatus'])
            search.frequency = search.frequency + 1
    except Search.DoesNotExist:
        search = Search(word_or_phrase=request.GET['query'],
                        committee=request.GET['decisionBodyId'],
                        from_date=request.GET['fromDate'],
                        to_date=request.GET['toDate'],
                        item_status=request.GET['itemStatus'])
    
    search.save()
    
    args = {'search_id': search.id, 'search_query': search.word_or_phrase}
    args.update(csrf(request))
    
    return render_to_response('list.html', args)

