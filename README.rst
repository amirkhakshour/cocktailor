cocktailor
==========

Get Awsome Refreshing Cocktail Recipes!

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


:License: MIT


Settings
--------



Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy cocktailor

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest


Deployment
----------

The following details how to deploy this application.



Local deployment
^^^^^^^^^^^^^^^^^^
::

    $ docker-compose -f local.yml build
    $ docker-compose -f local.yml up


Production deployment
^^^^^^^^^^^^^^^^^^^^^^^
::

    $ docker-compose -f production.yml build
    $ docker-compose -f production.yml up



using API
^^^^^^^^^^
1- create a token using username and password you've created during setup:

::

    $ curl -X POST -d "username=admin&password=admin" http://127.0.0.1:8000/auth-token/

2- use to auth token in response to access endpoints:

::

    $ curl http://127.0.0.1:8000/api/cocktail/ingredients/ -H 'Authorization: Token 00f8cd25a71451799f84cfa637a0ca29c829cea9'
