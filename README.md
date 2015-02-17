# Group Charlie Server Version

This is the server version of the Multi-Lingual SMS Project Implementation

## Install

The project uses Django as the server framework

### 1. Install Django

[Download Link: ](https://www.djangoproject.com/download/)
[Official Tutorials: ](https://docs.djangoproject.com/en/1.7/intro/tutorial01/)

Also install `django_tables2`

### 2. Setup the Database

By defualt a `sqlite` database will be used for storage. To set up the initial
database run:

```
python manage.py syncdb
```

To start a local test server:

```
python2 manage.py runserver
```

From then, go to localhost:8000 in chrome

## Upload Files

The question requires the following rendering pattern:

``label1: option11, option12; label2: option21, option22``

