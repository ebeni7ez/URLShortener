from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import resolve
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from .models import Link, Word
from .forms import LinkForm
import re
import string
from django.utils import timezone

COMMON_URL_STRINGS = ['http', 'www', 'org', 'com']

def substract_common_words(list):
    clean_list = [item for item in list if item not in COMMON_URL_STRINGS]
    return clean_list

def pick_random_word():
    list = Word.objects.filter(used=False)
    if (len(list)):
        return list[0]
    return None

def index(request):
    """
        Main page
    """
    ctx = {}
    ctx['form'] = LinkForm()

    if request.method == "POST":
        submit_form = LinkForm(request.POST)
        if submit_form.is_valid():
            url = submit_form .cleaned_data['url']

            # Find words in the URL
            word_list = re.findall('[%s]+' % string.ascii_letters, url)

            # Clean word list with reserved common words for URLs            
            word_list = substract_common_words(word_list)

            link = None
            word = None            
            for item in word_list:
                try:
                    elem = Word.objects.get(key=item)
                    if not elem.used:
                        word = elem
                        break
                except ObjectDoesNotExist:
                    continue

            if not word:
                word = pick_random_word()

            if word:               
                word.used = True
                word.save()
                link = Link(url=url, word=word)
                link.save()
            else:
                link = Link.objects.all().order_by('date_submitted')[0]
                link.url = url
                link.date_submitted = timezone.now()
                link.save()           

            ctx['url'] = link.url
            ctx['short_url'] = link.get_absolute_url(request)
            
        else: 
            ctx['form'] = submit_form 

    return render(request, 'urls/index.html', ctx)

def redirect_short_url(self, *args, **kwargs):
    """
        Shows the content from the 
        original URL
    """
    short_url = kwargs['short_url']
    url = Link.expand_url(short_url)
    return HttpResponseRedirect(url)
