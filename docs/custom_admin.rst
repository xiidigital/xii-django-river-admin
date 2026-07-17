.. _`Custom Admin`:

.. |Custom Workflow Name & Icon| image:: /_static/images/custom-admin-name-icon.png
.. |Custom List Workflow Ojbcets Pages| image:: /_static/images/custom-list-workflow-objects-page.png


Custom Admin
============

``xii-django-river-admin`` is also meant to be functioning like any other
django admin libraries but specificly for workflow operations.
You can definitely be using ``xii-django-river-admin`` as it comes but there
are quite cool customizations you can do with it.
The way how to customize it is very much like the way
how you customize your ``Django`` model admin. We kept the same
practice


.. code:: python

    # admin.py

    from xii.django_river_admin import RiverAdmin, site
    from examples.shipping_example.models import Shipping

    class ShippingRiverAdmin(RiverAdmin):
        name = "Shipping Flow"
        icon = "mdi-truck"
        list_displays = ['pk', 'product', 'customer', 'shipping_status']

    site.register(Shipping, "shipping_status", ShippingRiverAdmin)

.. note::
    ``xii-django-river-admin`` uses material icon sets. In order to see what icons you
    can use more please take a look at `Material Design Icons`_. What ever
    you want to use from there just add ``mdi-`` prefix to the icon name.

.. _Material Design Icons: https://materialdesignicons.com/

Here is the output;

|Custom Workflow Name & Icon|
|Custom List Workflow Ojbcets Pages|


Method Field
~~~~~~~~~~~~

``xii-django-river-admin`` supports custom field that can be fetched from
a python method instead of the workflow object itself like in
``Django`` model admins.



.. code:: python

    # admin.py

    from xii.django_river_admin import RiverAdmin, site
    from examples.shipping_example.models import Shipping

    class ShippingRiverAdmin(RiverAdmin):
        name = "Shipping Flow"
        icon = "mdi-truck"
        list_displays = ['custom_pk', 'product', 'customer', 'shipping_status']

        @classmethod
        def custom_pk(cls, obj):
            return "Primary Key: %d" % obj.pk


    site.register(Shipping, "shipping_status", ShippingRiverAdmin)
