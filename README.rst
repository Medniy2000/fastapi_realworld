FastAPI Real World
====================

FastAPI Real World description

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style

Run app local
^^^^^^^^^^^^^^

To run app local use::

    $ cd <path_to_app_root>
    $ cp .env.example .env

    # to run app perform:
        # install, run postgres, actualize .env

    $ uvicorn src.app.main:app --reload


API docs here::

    # http://127.0.0.1:8000/docs
    # http://127.0.0.1:8000/redoc

To make db schema::

    # use commands

    $ alembic revision --autogenerate -m "some message"
    $ alembic upgrade head


To check code quality[black, flake8, mypy]::

    # use commands

    $ bash beautify.sh


Docs commands::

    # before:
        # poetry add -D sphinx
        # mkdir docs
        # cd docs
        # poetry run sphinx-quickstart
    $ cd <path_to>/docs
    $ poetry run make html

Run tests::

    $ docker-compose -f docker-compose-tests.yml up --force-recreate --remove-orphans --renew-anon-volumes
