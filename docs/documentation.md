# ippcdj Documentation

## Installation / Setup

1. Install [Python](http://python.org) and [virtualenv](https://pypi.python.org/pypi/virtualenv), then open a terminal session and go to your projects directory, such as `~/projects`, and type the following command:

    `virtualenv ippcdj-env`
    
2. Add the following to the bottom of the `~/projects/ippcdj-env/bin/activate`  (in windows may `~/projects/ippcdj-env/Script/activate`) file then save the file:

    export DJANGO_SETTINGS_MODULE="ippcdj_repo.settings"
    echo $DJANGO_SETTINGS_MODULE
    
3. Back in the Terminal, activate the virtual environment:

    ````
    . bin/activate
    # in windows: . Scripts/activate
        
    git clone https://github.com/hypertexthero/ippcdj.git ippcdj_repo
    cd ippcdj_repo
    pip install -r requirements/project.txt
    # if you see errors related to PIL, see: <http://www.hypertexthero.com/logbook/2013/07/pil-pillow-libjpeg-ldconfig/>
    python manage.py createdb
    # Accept the defaults, say 'Yes' to 'fake initial migrations'
    python manage.py runserver
    
    ````

4. Go to 127.0.0.1:8000 to see the app running. go to 127.0.0.1:8000/admin to log in to the admin interface. To stop the server press Ctrl-C in the terminal.
    
## Data migrations using South app after changing models

Make sure 'south' is present in your INSTALLED_APPS IN settings.py.

If you add new fields or change certain values of existing ones such as blank or null in the ippc application, you need to do a data migration to synchronize the database:

1. If you followed the Installation / Setup steps above go to step 2. Otherwise run the following in the terminal:

    `./manage.py convert_to_south ippc`

2. Everytime you make a change in your models do the following:

    `./manage.py schemamigration ippc --auto`  
    `./manage.py migrate ippc`

3. If you want to rever to a previous migration, look for the previous migration number in ippc/migrations and replace #### with the migration number in the following command:

    `manage.py migrate your_app ####`

## Dumpdata

    `python manage.py dumpdata --indent 2 > initial_data.json`