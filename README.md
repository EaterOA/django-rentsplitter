Rentsplitter
===

Simple Django app for managing utility/debt expenses in an apartment, which are
used to split rent at the end of the month.

Frontend thrown together with Bootstrap.

Installation
===

Use like any Django app.

- Install the package with setuptools or copy the whole app over to the project directory
- Add "rentsplitter" to INSTALLED_APPS
- Add `url(r'^rent/', include('rentsplitter.urls'))`
- `python manage.py migrate`
