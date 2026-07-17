.. _`Contribute`:

Contribute
==========

``xii-django-river-admin`` consists of two parts that are backend and ui.
It is built with `Django Rest Framework`_ on the backend
side whereas Vue_ on the front end side.

Backend
-------
The backend side is built with ``Django``
and `Django Rest Framework`_. So you need ``Django``
development environment to be set up.

1. Install the dependencies

   .. code:: bash

       pip install -r requirements.txt

2. Install Tox_ to run the tests for all environments.

   .. code:: bash

       pip install tox

3. Install Twine_ and other necessary packages to upload packages to ``PyPI``

   .. code:: bash

       pip install build twine

4. You are ready to develop the backend side now.

Development
~~~~~~~~~~~

   .. code:: bash

       python manage.py runserver

Tests
~~~~~

Tox_ is used on the backend side to automate ``Python`` & ``Django``
testing. Tests are under ``xii/django_river_admin/tests/``. Simply run

   .. code:: bash

       tox

To run it for a specific environment;

   .. code:: bash

       tox -e py312-dj52

UI
--

The ui is built with Vue_ 3 + Vuetify 3 + Vite. So you need a
``Node.js``/Vue development environment to be set up.

1. Install ``node`` & ``npm``
2. Install ``yarn`` (`Install Yarn`_)
3. Install dependencies

   .. code:: bash

       yarn install


Development
~~~~~~~~~~~

While developing the front end ``Vue`` app,
you can run it without building it and the dev server will
automatically reload on any changes in the code (Vite's hot module
reload). This is quite a useful thing for fast feedback and debugging.
One thing you should make sure before you run this, backend server is
also running since it needs to call the backend

   .. code:: bash

       python manage.py runserver

   .. code:: bash

       cd ui
       yarn dev


Tests
~~~~~

UI tests are written with Vitest_ against Vue Test Utils. Tests are
under ``ui/tests/``.
To run the tests simply;

   .. code:: bash

       cd ui
       yarn test:unit

To run a specific one;

   .. code:: bash

       yarn test:unit StateInput.spec.js

To run the tests with fresh snapshots (to clean the snapshots);

   .. code:: bash

       yarn test:unit -u

Build
~~~~~

   .. code:: bash

       cd ui
       yarn build


The distribution folders of the ``Vue`` app are
``xii/django_river_admin/templates`` and ``xii/django_river_admin/static``.
The reason for that is because a ``Django`` app should
contains all the ``html`` and ``static`` files under
``templates`` and ``static`` folders.


.. _Vue: https://vuejs.org/
.. _`Install Yarn`: https://yarnpkg.com/en/docs/install
.. _`Django Rest Framework`: https://www.django-rest-framework.org/
.. _Vitest: https://vitest.dev/
.. _Tox: https://tox.readthedocs.io/en/latest/
.. _Twine: https://pypi.org/project/twine/