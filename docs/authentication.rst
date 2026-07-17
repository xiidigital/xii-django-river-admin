.. _authentication:

.. |Login Page Img| image:: /_static/images/login.png


Authentication
==============


``xii-django-river-admin`` is working like an administration interface
and naturally it has an authentication mechanism.
Even though it is working with the users  who are created
via Django API, it doesn't use Django Admin logged in your
Django admin. So you will be asked to login with your user;


|Login Page Img|

.. note::
    In order to be able to login, your user has to be either
    an admin user or have the ``xii_django_river.view_workflow``
    permission. So to speak, ``xii_django_river.view_workflow`` is the
    minimum required permission to be able to use
    ``xii-django-river-admin``.


Once user is logged in, they won't be asked by their credentials
until they are logged out or their minimum required permission
described above is revoked.

Every API endpoint behind the login screen also requires the caller to be
authenticated at the server level (``IsAuthenticated`` by default) - the
frontend's login gate isn't the only thing standing between an anonymous
caller and the data. Endpoints that create, update, delete, or approve
something additionally require the specific Django permission for that
action (e.g. ``xii_django_river.add_state``,
``xii_django_river.approve_function``).

.. toctree::
   :maxdepth: 2
