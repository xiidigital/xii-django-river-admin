.. _`Create or Update Function`:

.. |Create Function| image:: /_static/images/create-function.png

Create & Update Function
========================

.. note::
    ``xii-django-river-admin`` is not extending the APIs of ``xii-django-river``.
    In order to see how your functions should look like please
    visit the `xii-django-river function documentation`_ itself

.. note::
    In order to see this page, your user has to have
    ``xii_django_river.add_function`` permission.


.. _xii-django-river function documentation: https://github.com/xiidigital/xii-django-river/blob/master/docs/hooking/function.rst

|Create Function|

.. note::
    Changes on the functions are applied to your hooks right away.
    It means that, next time a hook is kicked in with this function
    will be executed with the up to date version of the function.
