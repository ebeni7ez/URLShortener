from django.test import TestCase
from django.core.urlresolvers import reverse, resolve
from .models import Link, Word
from django.utils import timezone
import random
import string


class ShortenedURL(TestCase):
    def setUp(self):
        word = Word(key="python",used=False)
        word.save()
        url = "http://python.org/"
        date_submitted = timezone.now()
        link = Link(url=url, word=word, date_submitted=date_submitted)
        link.save()
    
    def test_shorter(self):
        """
            Tests the returned URL is shorter
            than the original URL
        """
        url = "http://python.org/"
        link = Link.objects.get(url=url)
        short_url = Link.short(link)
        self.assertLess(len(short_url), len(url))

    def test_expand_url(self):
        """
            Tests the returned URL is shorter
            than the original URL
        """
        url = "http://python.org/"
        link = Link.objects.get(url=url)
        short_url = Link.short(link)

        # the short url is expanded when accessed
        redirect_url = Link.expand_url(short_url)
        self.assertEqual(url, redirect_url)

    def test_redirect_to_original_site(self):
        """
            Test that the submiting form
            returns a valid short link
            that redirects to the original
            website
        """
        url = "http://python.org/"
        link = Link.objects.get(url=url)
        short_url = Link.short(link)

        response = self.client.get(reverse('redirect_short_url',
                                       kwargs={"short_url": short_url}))
        self.assertRedirects(response, url)

    def test_index_page(self):
        """
            Tests a index page exists
            and contains the URL form.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_submit_form_word_not_list(self):
        """
            Test that the submitting form
            returns the short url
        """
        word = Word(key="word",used=False)
        word.save()

        url = "http://mydomain.org/word"
        response = self.client.post(reverse('index'),
                                        {"url": url}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("url", response.context)

        link = Link.objects.get(url=response.context["url"])
        short_url = Link.short(link)
        self.assertEqual(url, link.url)
        self.assertEqual(short_url, word.key)
        self.assertIn(short_url, response.context["short_url"])

    def test_submit_form_word_not_in_list(self):
        """
            Test that the submitting form return
            the short url
        """
        url = "http://mydomain.org/"
        response = self.client.post(reverse('index'),
                                        {"url": url}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("url", response.context)

        link = Link.objects.get(url=response.context["url"])
        short_url = Link.short(link)
        self.assertEqual(url, link.url)
        self.assertIn(short_url, response.context["short_url"])

    def test_short_and_expand_link_n_times(self):
        """
            Test when submitting multiple links
        """
        TIMES = 1000 #30000
        for i in xrange(TIMES):
            uri = "".join(random.sample(string.ascii_letters, 10))
            url = "http://mydomain.com/{}/".format(i, uri)
            response = self.client.post(reverse('index'),
                                        {"url": url}, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn("url", response.context)

            link = Link.objects.get(url=response.context["url"])
            short_url = Link.short(link)
            long_url = Link.expand_url(short_url)
            self.assertEqual(url, long_url)
