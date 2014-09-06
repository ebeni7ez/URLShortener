=== Clone the Project ===

$ git clone https://github.com/ebeni7ez/URLShortener

=== Set the environment ===

Install virtualenvwrapper. 

$ pip install virtualenvwrapper

$ source /usr/local/bin/virtualenvwrapper.sh

$ mkvirtualenv urlshort

$ workon urlshort

=== Install the requirements ===

$ cd URLShortener
$ pip install -r requirements.txt

=== Install the requirements ===

$ cd urlshortener
$ python manage.py syncdb
$ python manage.py migrate

=== Run in your local server and access ===

$ python manage.py runserver

Go to your browser and visit http://localhost:8000

===Run the tests===

$ python manage.py test urls






