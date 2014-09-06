from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


class Word(models.Model):
    key = models.CharField(max_length=20, primary_key=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.key


class Link(models.Model):
    word = models.OneToOneField(Word, primary_key=True)
    url = models.URLField()
    date_submitted = models.DateTimeField(default=timezone.now)

    class Meta:
        get_latest_by = 'date_submitted'

    @staticmethod
    def short(link):        
        return link.word.key

    @staticmethod
    def expand_url(short_url):
        try:
            word = Word.objects.get(key=short_url)
            link = Link.objects.get(word=word)
            return link.url
        except ObjectDoesNotExist as e:
            raise Http404

    def get_absolute_url(self, request):
        return request.build_absolute_uri(self.word.key) 

