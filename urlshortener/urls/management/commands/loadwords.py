"""
    Command that cleans all the words
    from one or more file, and load them
    into the database.

    All words to lowercase stored in the
    database are being converted to
    lowercase and removing any characters
    that are not [0-9a-z]
"""

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from urls.models import Word
import sys
import logging

class Command(BaseCommand):
    args = '<file>'
    help = 'Load words from one or more given files'

    def handle(self, *args, **options):
        if len(args) == 0:
            logging.error('Got no or invalid arguments, exiting.')
            sys.exit(1)

        for filename in args:
            with open(filename, 'r') as f:
                for word in f:
                    # removes break lines and convert to lowercase
                    word = self.convert_string(word)     
                    print word              

                    # stores the word in the database
                    try:
                        Word.objects.create(key=word)
                    except IntegrityError:
                        continue
        return

    def convert_string(self, word):
        word = word.rstrip('\n').lower()
        # removes special characters
        word = ''.join(e for e in word if e.isalnum())
        return word
