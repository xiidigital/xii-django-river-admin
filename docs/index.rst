.. |Build Status| image:: https://github.com/xiidigital/xii-django-river-admin/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/xiidigital/xii-django-river-admin/actions/workflows/ci.yml

.. |Licence| image:: https://img.shields.io/github/license/xiidigital/xii-django-river-admin
    :alt: GitHub license
    :target: https://github.com/xiidigital/xii-django-river-admin/blob/master/LICENSE

.. |Downloads| image:: https://img.shields.io/pypi/dm/xii-django-river-admin
    :alt: PyPI - Downloads

.. |Timeline Img| image:: /_static/images/timeline-in-macbook.png

.. |Home Img| image:: /_static/images/home-left-panel-on-in-macbook.png

.. |Re-prio Img| image:: /_static/images/re-prioritization-in-macbook.png

.. |Workflow Edit Img| image:: /_static/images/edit-workflow-in-macbook.png

.. |Images| image:: /_static/images/readme-images.gif



xii-django-river-admin
=======================

.. rst-class:: center-without-bg

|Build Status| |Licence| |Downloads|

``xii-django-river-admin`` is a very modern and
a shiny customizable admin extension with user friendly and easy to use
interfaces for xii-django-river_ (XII Digital's fork of django-river,
modernized for Django 4.2-6.0 and Python 3.10-3.13). It is the matching
fork of the original river-admin_ project. The power of it comes from
the libraries it uses on both backend and frontend sides which are
``xii-django-river``, ``django-rest-framework``, ``Vue 3`` and ``Vuetify 3``.

.. rst-class:: center-without-bg

|Images|

.. _xii-django-river: https://github.com/xiidigital/xii-django-river/
.. _river-admin: https://github.com/javrasya/river-admin

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

Getting Started
===============

You can easily get started with ``xii-django-river`` by
following :ref:`getting-started`.

Contents
========

.. toctree::
   :maxdepth: 2

   getting_started
   authentication
   workflow/index
   function/index
   custom_admin
   workflow_object/index
   contribute


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
