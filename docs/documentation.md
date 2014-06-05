# ippcdj Documentation

## Installation / Setup


1. Install Django development environment on your computer and follow instructions to get it running: <http://wiki.bitnami.com/Infrastructure_Stacks/BitNami_Django_Stack>

2. Clone code repository (currently on GitHub), move into it and install third-party libraries for the project:

    ````
    git clone https://github.com/hypertexthero/ippcdj.git ippcdj_repo
    cd ippcdj_repo
    pip install -r requirements/project.txt
    # if you see errors related to PIL, see: <http://www.hypertexthero.com/logbook/2013/07/pil-pillow-libjpeg-ldconfig/>
    # if you're on Windows install Pillow for your computer from <http://www.lfd.uci.edu/~gohlke/pythonlibs/> (see <https://bitnami.com/forums/forums/djangostack/topics/i-was-running-through-the-djangobook-tutorials-and-now-i-need-a-python-imaging-library>)
    
    # rename local_settings_example.py to local_settings.py 
    mv local_settings_example.py local_settings.py 
    
    # create database (or rename existing test one dev.dbcopy > dev.db)
    python manage.py createdb
    
    # Accept the defaults, say 'Yes' to 'fake initial migrations'
    python manage.py runserver
    
    ````

3. Go to 127.0.0.1:8000 to see the app running. go to 127.0.0.1:8000/admin to log in to the admin interface. To stop the server press Ctrl-C (Ctrl-Z and Enter in Windows) in the terminal.
    
## Workflow

=TODO

1. GitHub or Git on Dev server?
2. Git workflow

    a. [Branching](http://git-scm.com/book/en/Git-Branching-Basic-Branching-and-Merging)?
    b. Etc.
    
2. Dev > Production deployment

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

## Update translations for non-user-generated site content

<https://docs.djangoproject.com/en/dev/topics/i18n/translation/>

Edit the django.po file for each language in `ippcdj_repo/conf/locale/` and then run the following commands in the terminal to compile the translation files: 

    `python manage.py makemessages --all`
    `python manage.py compilemessages`
