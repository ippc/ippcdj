# ippcdj Documentation

## Data migrations using South app after changing models

Make sure 'south' is present in your INSTALLED_APPS IN settings.py.

After you created your app and added some fields, you decid to add a new field.

First make sure that your app is already converted to south, if not just run:

  ./manage.py convert_to_south appname

Now everytime you make a change in your models do the following:

  ./manage.py schemamigration appname --auto
  ./manage.py migrate appname
