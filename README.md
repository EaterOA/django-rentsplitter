Rentsplitter
===

Simple Django app for managing utility/debt expenses in an apartment, which are
used to split rent at the end of the month.

Frontend thrown together with Bootstrap.

Installation
===

Install like any Django app.

- Install the package with setuptools or copy the whole app over to the project directory
- Add "rentsplitter" to INSTALLED_APPS
- Add `url(r'^rent/', include('rentsplitter.urls'))`
- `python manage.py migrate`
- `python manage.py collectstatic`

The Rent and Users need to be added manually. Enter `python manage.py shell`
and type:

    from rentsplitter.model import User, Rent
    Rent(amount=1234).save()
    User(name="Alice").save()
    User(name="Bob").save()
    # ...
