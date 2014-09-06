=== Clone the Project ===

$ git clone https://github.com/ebeni7ez/URLShortener

=== Set the environment ===

Install virtualenvwrapper. 

$ pip install virtualenvwrapper

$ source /usr/local/bin/virtualenvwrapper.sh

$ mkvirtualenv urlshort

workon urlshort

=== Install the requirements ===

$ pip install -r requirements.txt

=== Install the requirements ===

$ ./manage.py syncdb
$ ./manage.py migrate

=== Run in your local server and access ===

$ ./manage.py runserver

Go to your browser and visit http://localhost:8000

===Run the tests===

$ ./manage.py test urls






