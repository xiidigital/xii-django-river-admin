.. _getting-started:

.. |Issue Tracking Workflow Img| image:: /_static/images/issue-tracking-workflow.png
.. |Shipping Workflow Img| image:: /_static/images/shipping-workflow.png


Getting Started
===============

Requirements
------------

* `xii-django-river`_ >= 4.0.0
* Python 3.10+ (whatever is supported by `xii-django-river`_)
* Django 4.2-6.0 (whatever is supported by `xii-django-river`_)
* Any browser that is supported by `Vuetify`_ (`Browser Support`_)

.. _`Browser Support`: https://vuetifyjs.com/en/getting-started/browser-support#browser-support
.. _`Vuetify`: https://vuetifyjs.com/en/
.. _`xii-django-river`: https://github.com/xiidigital/xii-django-river

Installation
------------
.. note::
    Before you can set up your workflow, your app
    integration with ``xii-django-river`` must be done.
    Don't worry it is with the easiest setup. To see
    how to do it with ``xii-django-river`` please have a
    look at `xii-django-river`_

1. Install and enable it

   .. code:: bash

       pip install xii-django-river-admin


   .. code:: python

       # settings.py

       INSTALLED_APPS=[
           ...
           'xii.django_river',
           'rest_framework.authtoken',
           'xii.django_river_admin',
           ...
       ]

       REST_FRAMEWORK = {
           'DEFAULT_AUTHENTICATION_CLASSES': [
               'rest_framework.authentication.BasicAuthentication',
               'rest_framework.authentication.TokenAuthentication',
           ],
           'EXCEPTION_HANDLER': 'xii.django_river_admin.views.exception_handler'
       }

2. Do migration;

   .. code:: bash

        python manage.py migrate

3. Register ``xii-django-river-admin`` urls in your app ``urls.py``

   .. code:: python

        from django.urls import include, re_path

        urlpatterns = [
            re_path(r'^', include("xii.django_river_admin.urls")),
        ]

4. Collect statics and make sure ``STATIC_URL`` is ``/static/`` **(FOR PRODUCTION WHERE DEBUG=False)**;

   .. code:: bash

       python manage.py collectstatic --no-input --no-post-process

5. Run your application;

   .. code:: bash

       python manage.py runserver 0.0.0.0:8000


6. Open it up on the browser and login with an admin user and enjoy the best way of flowing your work ever :-)

   .. code:: bash

       http://0.0.0.0:8000/xii-django-river-admin/

Out of the Box Examples
-----------------------

``xii-django-river-admin`` comes with a few examples that you can
fiddle with and find your way easier.


.. note::
    Enabling them will create their tables and
    also the necessary workflow components in
    the DB for you. It might be good idea to try
    them out on a development database.

Shipping Flow
^^^^^^^^^^^^^

Enable the example app and then run your application

   .. code:: python

       # settings.py

       INSTALLED_APPS=[
           ...
           'xii.django_river',
           'rest_framework.authtoken',
           'xii.django_river_admin',
           'examples.shipping_example',
           ...
       ]

   .. code:: bash

        python manage.py migrate
        python manage.py bootstrap_shipping_example

|Shipping Workflow Img|

Issue Tracking Flow
^^^^^^^^^^^^^^^^^^^

Enable the example app and then run your application

   .. code:: python

       # settings.py

       INSTALLED_APPS=[
           ...
           'xii.django_river',
           'rest_framework.authtoken',
           'xii.django_river_admin',
           'examples.issue_tracker_example',
           ...
       ]

   .. code:: bash

        python manage.py migrate
        python manage.py bootstrap_issue_tracker_example

|Issue Tracking Workflow Img|


.. toctree::
   :maxdepth: 2
