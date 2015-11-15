from django.db import models

class Search(models.Model):
    word_or_phrase = models.CharField(max_length=200)
    committee = models.CharField(max_length=200)
    from_date = models.CharField(max_length=200)
    to_date = models.CharField(max_length=200)
    item_status = models.CharField(max_length=200)
    
    recent_result = models.CharField(max_length=200, default='')
    
    frequency = models.IntegerField(default=1)
    
    def __unicode__(self):
        return "%s (%s)" % (self.word_or_phrase, str(self.frequency))


class Registration(models.Model):
    email = models.EmailField()
    search_id = models.ForeignKey('Search')
    
    activated = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=200, default='')
    
    last_result = models.CharField(max_length=200, default='')
    
    agenda_list = models.TextField(default='')
    
    def __unicode__(self):
        return "%s (%s)" % (self.email, str(self.search_id))

