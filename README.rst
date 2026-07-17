.. |Build Status| image:: https://github.com/xiidigital/xii-django-river-admin/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/xiidigital/xii-django-river-admin/actions/workflows/ci.yml

.. |Licence| image:: https://img.shields.io/github/license/xiidigital/xii-django-river-admin
    :alt: GitHub license
    :target: https://github.com/xiidigital/xii-django-river-admin/blob/master/LICENSE

.. |Downloads| image:: https://img.shields.io/pypi/dm/xii-django-river-admin
    :alt: PyPI - Downloads

.. |Logo| image:: docs/logo.svg
    :width: 200

.. |Images| image:: docs/_static/images/readme-images.gif

.. |Issue Tracking Workflow Img| image:: docs/_static/images/issue-tracking-workflow.png

.. |Shipping Workflow Img| image:: docs/_static/images/shipping-workflow.png

xii-django-river-admin
=======================

|Build Status| |Licence| |Downloads|

\:rocket\: \:rocket\: \:rocket\: ``xii-django-river-admin`` is a very modern and
a shiny customizable admin extension with user friendly and easy to use
interfaces for xii-django-river_ (XII Digital's fork of django-river,
modernized for Django 4.2-6.0 and Python 3.10-3.13). This is the matching
fork of the original river-admin_ project, kept in sync with
xii-django-river_'s API and app label rather than the other way around.
The power of it comes from the libraries it uses on both backend and
frontend sides: ``xii-django-river``, ``django-rest-framework``, ``Vue 3``
and ``Vuetify 3``.

.. _`Browser Support`: https://vuetifyjs.com/en/getting-started/browser-support#browser-support
.. _`Vuetify`: https://vuetifyjs.com/en/
.. _`xii-django-river`: https://github.com/xiidigital/xii-django-river
.. _`river-admin`: https://github.com/javrasya/river-admin

|Images|

Demo
====

There is no hosted public demo for this fork. To run the bundled demo
locally instead:

   .. code:: bash

        export LOCAL_DEMO=True
        pip install -r requirements.txt
        python manage.py migrate
        python manage.py bootstrap_shipping_example
        python manage.py bootstrap_issue_tracker_example
        python manage.py bootstrap_river_admin_demo
        python manage.py runserver

And then go to ``http://127.0.0.1:8000/xii-django-river-admin/``

**Note:** Create an admin user for yourself if you would like more access.


Documentation
-------------

Documentation lives under `docs/`_ in this repository (Sphinx sources) and
is published to `GitHub Pages`_ on every push to ``master`` via
``.github/workflows/docs.yml``.

.. _`docs/`: https://github.com/xiidigital/xii-django-river-admin/tree/master/docs
.. _`GitHub Pages`: https://xiidigital.github.io/xii-django-river-admin/

Getting Started
===============

Requirements
------------

* `xii-django-river`_ >= 4.0.0
* Python 3.10+ (whatever is supported by `xii-django-river`_)
* Django 4.2-6.0 (whatever is supported by `xii-django-river`_)
* Any browser that is supported by `Vuetify`_ (`Browser Support`_)

Installation
------------

**Note:** Before you can set up your workflow, your app
integration with ``xii-django-river`` must be done.
Don't worry it's pretty trivial to set it up. To see
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

**Note:** Enabling them will create their tables and
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

Contribute
==========

In order to contribute, fork the repository, look at every instructions
in CONTRIBUTE_ before you work then commit your changes and send a pull
request.

Make sure you add yourself to CONTRIBUTORS_.

.. _CONTRIBUTE: https://github.com/xiidigital/xii-django-river-admin/blob/master/docs/contribute.rst
.. _CONTRIBUTORS: https://github.com/xiidigital/xii-django-river-admin/blob/master/CONTRIBUTORS

.. _license:

License
=======

This software is licensed under the `New BSD License`.
See the `LICENSE FILE`_ file in the top distribution directory
for the full license text.

.. _`LICENSE FILE`: https://github.com/xiidigital/xii-django-river-admin/blob/master/LICENSE
