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
    """
        Substracts the common strings
        that appear on every url from
        the word list extracted from
        the given URL
    """
    clean_list = [item for item in list if item not in COMMON_URL_STRINGS]
    return clean_list

def pick_random_word():
    """
        Picks a random word from the database
        that has not been used for other
        short url
    """
    list = Word.objects.filter(used=False)
    if (len(list)):
        return list[0]
    return None

def create_link(url):
    """
        Receives an URL and returns a Link
        object already stored in the 
        database
    """
    # Find words in the URL
    word_list = re.findall('[%s]+' % string.ascii_letters, url)

    # Clean word list with reserved common words for URLs
    word_list = substract_common_words(word_list)

    link = None
    word = None

    # Looks for a word in the database that has not been
    # used and appears in the given URL
    for item in word_list:
        try:
            elem = Word.objects.get(key=item)
            if not elem.used:
                word = elem
                break
        except ObjectDoesNotExist:
            continue

    # If a word hasn't been found, look for another word
    # in the database that has not been used
    if not word:
        word = pick_random_word()

    if word:               
        word.used = True
        word.save()
        link = Link(url=url, word=word)
        link.save()
    else:
        # If all the word in the database has been used already,
        # look for the oldest link that has been shortened
        # and replace it
        link = Link.objects.all().order_by('date_submitted')[0]
        link.url = url
        link.date_submitted = timezone.now()
        link.save()
    return link

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
            link = create_link(url)
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
