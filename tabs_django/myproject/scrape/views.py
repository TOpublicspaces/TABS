# Create your views here.

from bs4 import BeautifulSoup
from twill.commands import *
from twill import set_output as shutup_twill
from StringIO import StringIO
from functools import partial

from django.shortcuts import render_to_response, redirect
from django.utils import simplejson
from django.http import HttpResponse

from main.models import Search

def perform_search(word_or_phrase, committee, from_date, to_date, item_status):
    
    # Silence twill
    shutup_twill(StringIO())
    
    # Grab the voting form
    go("http://app.toronto.ca/tmmis/findAgendaItem.do?function=doPrepare")
    fill = partial(fv,1)

    # Fill out the form with the id, and set it to download
    fill("word_or_phrase", word_or_phrase)
    if committee:
        fill("decision_body",committee)
    fill("fromDate",from_date)
    fill("toDate",to_date)
    fill("item_status",item_status)
    # Define more search restrictions here...
    
    submit()
    soup = BeautifulSoup(show())

    rows = soup.find("table", {"id": "searchResultsTable"}).find_all("tr")[1:]

    agenda_items = []

    for result in rows:
        meeting_date = result.find("td", {"class": "meetingDate"}).get_text()
        item_num = result.find("td", {"class": "reference"}).find("a").get_text()
        item_url = "http://app.toronto.ca" + str(result).split('(')[1].split(')')[0][1:-1]
        title = result.find("td", {"class": "agendaItemTitle"}).get_text()
        committee = result.find("td", {"class": "decisionBodyName"}).get_text()
        agenda_items.append({'meeting_date': meeting_date,
                             'item_num': item_num,
                             'item_url': item_url,
                             'title': title,
                             'committee': committee})
    
    return agenda_items


def query(request):
    assert request.method == 'GET'
    assert 'search_id' in request.GET
    q = Search.objects.get(id=int(request.GET['search_id']))
    results = perform_search(q.word_or_phrase,
                             q.committee, 
                             q.from_date,
                             q.to_date,
                             q.item_status)
    q.recent_result = hash(','.join([str(i['item_num']) for i in results]))
    q.save()
    return HttpResponse(simplejson.dumps(results), 'application/javascript')



