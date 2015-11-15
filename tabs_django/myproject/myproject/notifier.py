import sys, datetime
sys.path.append("/home/tpsi/webapps/tabs_django/lib/python2.7/")
sys.path.append("/home/tpsi/webapps/tabs_django/myproject/")

from django.core.management import setup_environ
import settings

setup_environ(settings)

from django.core.mail import send_mail

from main.models import Registration, Search
from scrape.views import perform_search

def send_update(email, search_id, word_or_phrase, activation_key, mapping, new_items):
    message = "Hello,\n"
    message += "  New information on a search you made is available."
    message += " The following are the new agenda items that have matched"
    message += " your search for '%s':\n\n" % word_or_phrase
    for item in new_items:
        message += "(%s) %s\n" % (item, mapping[item]['title'])
        message += "Committee: %s\n" % mapping[item]['committee']
        message += "Agenda URL: %s\n\n" % mapping[item]['item_url']
    message += " Please check out the following url for the entire search:\n- "
    message += 'http://www.tabstoronto.com/search/?search_id=' + str(search_id)
    message += "\n\n To unsubscribe to this search, go to the following url:\n- "
    message += 'http://www.tabstoronto.com/unsubscribe/' + activation_key + '/'
    print "\nSending %d items to %s for search '%s' (%s)...\n" % (len(new_items), email, str(word_or_phrase), str(search_id))
    send_mail('[tabsto] New agenda items!', message, 'notifications@tabstoronto.com',
              [email], fail_silently=False)

print "(%s) Checking for new updates..." % str(datetime.datetime.now())

# Check every search registration
for reg in Registration.objects.all():
    
    # Make sure the search term is active
    if reg.activated:
        
        search = reg.search_id

        print ">%s" % str(reg.email)
        
        results = perform_search(search.word_or_phrase,
                                 search.committee, 
                                 search.from_date,
                                 search.to_date,
                                 search.item_status)
        
        result_mapping = {}
        for res in results:
            assert '/' not in res['item_num'], "Uh oh: %s" % str(res['item_num'])
            result_mapping[res['item_num']] = res
        
        old = set(reg.agenda_list.split('/'))
        new = set(result_mapping.keys())
        
        search.recent_result = hash(','.join(sorted(result_mapping.keys())))
        search.save()
        
        if '' == reg.last_result:
            reg.last_result = search.recent_result
            reg.save()
        
        # Check to see if the latest was sent already
        if str(search.recent_result) != str(reg.last_result):
            if (new - old):
                send_update(str(reg.email), str(reg.search_id.id), str(search.word_or_phrase), str(reg.activation_key), result_mapping, (new-old))
            else:
                print "New hash, but no change for %s:" % str(reg.email)
                if (old - new):
                    print "Old items deleted: %s" % str(old - new)
                else:
                    print "Unknown hash diff..."
            
            # Always update -- just to clean up the false positives
            reg.last_result = search.recent_result
        
        reg.agenda_list = '/'.join(sorted(list(new)))
        reg.save()

    
print ''

