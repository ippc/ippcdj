# IPPC 4.0

## Things to do

- Setup Dev [MySQL](http://www.tecmint.com/install-mariadb-in-linux/), [php](http://www.if-not-true-then-false.com/2011/install-nginx-php-fpm-on-fedora-centos-red-hat-rhel/) and [phpmyadmin](http://stackoverflow.com/questions/5895707/how-to-combine-django-and-wordpress-based-on-ubuntu-and-nginx)
- Create remaining forms for all types of NPPO reports
    - Add [tagging](http://django-taggit.readthedocs.org/en/latest/) (keywords) and other fields
- Country pages:
    - Versioning of Pest Reports. Report number: GBR-32/1. When edited: GBR-32/2.
    - Other country forms
    - Prevent hidden report titles from appearing in search results
    - Country RSS feeds
- Author field for publications
- Homepage design
    - ¿'Add Pest Report' button in countries for NPPOs, visible even when user is logged out. Once user logs in, if they're an NPPO, they are redirected to the pest report form for their country?
    - Photos
- [Calendar](https://github.com/shurik/mezzanine.calendar) (or [Events](https://github.com/stbarnabas/mezzanine-events)?)
- [Forums](https://github.com/hovel/pybbm)
- User registration open but behind login-required and super-user required so only admins can add new users, who get notification emails to confirm account and set own password. OR, user registration open to all, but need approval by admins. i.e. Account registration & [activation](http://mezzanine.jupo.org/docs/user-accounts.html#account-approval) system?
    - Setup auto-sending of messages to new users, with possible custom messages for NPPOs and Editors
- [Single Sign-On](https://docs.djangoproject.com/en/1.5/topics/auth/customizing/). Create separate Accounts database to be used by all IPPC-related apps for authentication and authorization. The database should contain two tables:
    - Users (authentication - recognizes who you are)
        - ID
        - first name
        - last name
        - login/nickname
        - email
        - hashed password
        - salt
        - creation timestamp
        - update timestamp
        - account state (verified, disabled, etc)
    - Groups (knows what you are allowed to do, or what you allow others to do)

    Then, each application contains a profile app that extends the above Accounts DB authentication defaults:
    
    - IPPC
        - User(Fk to Accounts)
        - IPPC Country
        - Telephone
        - Alternate email
    - Phyto
        - User(Fk to Users)
        - CV
        - Date Joined
    - Ocs
        - User(Fk to Users)
        - Document Title
        - Revision
        - Comment
        - Version
    - Apppc
        - User(Fk to Users)
        - APPPC country

- [IRSS](https://github.com/ASKBOT/askbot-devel) refactor

    The easiest way to implement this is probably to use [CAS-Provider and CAS-consumer](http://stackoverflow.com/a/4663223) or [django-cas](https://bitbucket.org/cpcc/django-cas/overview). Another option: [mama-cas](https://github.com/jbittel/django-mama-cas). Relevant documentation pages: [multiple databases](https://docs.djangoproject.com/en/1.5/topics/db/multi-db/), [authentication](https://docs.djangoproject.com/en/1.5/topics/auth/customizing/), [multiple sites framework](https://docs.djangoproject.com/en/1.5/ref/contrib/sites/). See also [this blog post](http://reinout.vanrees.org/weblog/2014/05/09/authentication-python-web.html).
    
    Both phytosantiary.info and apppc.org will need to get SSL certificates for single sign-on to work securely: 
    
    > Even if the authentication with CAS is made using a mechanism which makes it difficult to interfere with, all authorized communication will subsequentely use a cookie identifing the session which can be used to hijack the connection. So you need to encrypt the communication. There is just no way around that if you want to enforce some sort of security.
    
- [Email utility](https://github.com/pinax/django-mailer)
    - Ability to insert user groups as well as individual users in `To:` field in `/admin/mailer/message/add/`
        - Use [admin actions](https://docs.djangoproject.com/en/1.5/ref/contrib/admin/actions/)?
        - [Custom admin form](http://stackoverflow.com/a/6099360/412329) overriding mailer's default form? Also see [this](http://djangosnippets.org/snippets/1650/) and [this](https://gist.github.com/luzfcb/1712348)
        - Custom email utility app and admin form calling django-mailer and groups?
- Add [blog category management page to admin](http://127.0.0.1:8000/en/admin/blog/blogcategory/)
- Contact form
- FAQ
- Custom Work Area main page descriptions or announcements or links to particular utilities depending on user permissions. Probably need to use a custom template that appears on /work-area/ URL (like the /news/ which displays the custom blog).
- Last modified date for pages
- Content (data) migration
- ¿Use jQuery [multi-file-upload](https://github.com/sigurdga/django-jquery-file-upload) functionality for uploading images and files to be inserted in pages and blog posts, [with additional fields for each file](https://github.com/blueimp/jQuery-File-Upload/wiki/How-to-submit-additional-form-data) if required?
- Order permission groups alphabetically in admin
- Setup proper permissions (nginx is currently running as root — not good) so that static media, including user-uploaded files are served through Nginx. Document nginx/gunicorn/supervisor setup (currently running gunicorn with deprecated `gunicorn_django -b 0.0.0.0:8000` command — get it running and working with recommended command instead)
- Setup working fabric script for easy deployment that does the following after running `fab deploy dev`:
    1. Adds, commits and pushes files to Github (for future: if tests pass)
    2. Logs in to dev.ippc.int, activates application virtualenv and pulls changes from Github
    3. Collect static files to locations to be served on dev server
    4. Restart gunicorn and nginx 
- Update to latest version of Mezzanine and make sure current functionality works
- [Versioning](https://django-simple-history.readthedocs.org/en/latest/) of all page content?
- [Pest Report mapping](http://leafletjs.com/examples/choropleth.html)
    - <http://blog.thematicmapping.org/2008/04/thematic-mapping-with-geojson.html>
    - <http://blog.thematicmapping.org/2012/11/how-to-minify-geojson-files.html>
    - Examples:
        - [Geochart](https://developers.google.com/chart/interactive/docs/gallery/geochart)
        - [Income levels example](http://humangeo.github.io/leaflet-dvf/examples/html/incomelevels.html)
        - [Top Cities](http://techslides.com/leaflet-map-with-utfgrid-and-php-served-mbtiles/)
- [Download multiple files](http://stackoverflow.com/a/12951557/412329)
- Use [Chosen](http://harvesthq.github.io/chosen/) to make globalnav dropdowns friedly. Also in admin. There's a [Django app](https://github.com/theatlantic/django-chosen), too. 
- Remove dropdown from Countries globalnav menu

## Installation / Setup


1. Install Django development environment on your computer and follow instructions to get it running: <http://wiki.bitnami.com/Infrastructure_Stacks/BitNami_Django_Stack>

2. Clone code repository (currently on GitHub), move into it and install third-party libraries for the project:

    ````
    git clone https://github.com/hypertexthero/ippcdj.git ippcdj_repo
    cd ippcdj_repo
    pip2.7 install -r requirements/project.txt
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

GitHub accounts are for codebase repository. Copies of codebase repository are also available in: 

1. Each developer's computer
2. dev.ippc.int server
3. ippc.int server

We're using a [**hared repository** model](https://help.github.com/articles/what-is-a-good-git-workflow) and the main IPPC code is at 

## GitHub Flow (how to work on www.ippc.int code):

First, [setup git](https://help.github.com/articles/set-up-git) (so you don't have to keep putting in  your password every time).

Then, [here's a basic guide](http://rogerdudler.github.io/git-guide/) (below is an example of working with this repository itself).

![](workflow.jpg "Drawing by Paola Sentinelli")


## Git Workflow

1. If you're working on the code for the first time, first clone repository from ippc repo (the first time you start working with it)

    ```bash    
    # change into your local projects directory (in your own computer) 
    cd ~/projects
    # clone the ippc repository
    git clone https://github.com/ippc/ippcdj.git
    ```

2. Before beginning the day's work, pull the latest changes from the online repo

   ```bash
   git pull

3. Change to ippcdj_repo directory and open the directory with your text editor (in this case, mate == textmate editor)  

    ```bash    
    cd ippcdj_repo && mate .
    ```

3. At end of day or more often as you prefer, add your changes to your local staging area and commit them to your local repo

    ```bash    
    git add .
    git commit -m 'new work'
    ```

4. Push your changes to main server at end of day (or more often)


    ```bash
    git push origin master
    ```
    
### Branching

1. Create a new branch called 'newfeature' and switch to it

    ```bash    
    git checkout -b newfeature
    ````
    
2. Create a new file for this new feature and add some text to it

    ```bash    
    echo 'a text file!' >> newfile.txt
    ````

3. At end of day or more often as you prefer, commit the changes to this branch

    ```bash    
    git add .
    git commit -m 'new feature'
    ````

4. Push your branch to main repo at end of day (or more often)

    ```bash    
    git push origin newfeature
    ````

### More information

- [Understanding the GitHub Flow](https://guides.github.com/introduction/flow/) (brief visual overview)
- [GitHub Flow in the Browser](https://help.github.com/articles/github-flow-in-the-browser) (In-browser GitHub features)
- [GitHub Flow](http://scottchacon.com/2011/08/31/github-flow.html) (detailed overview)
- [Pull new updates from original Github repository into forked Github repository](http://stackoverflow.com/a/3903835)
- [Git for beginners](http://stackoverflow.com/questions/315911/git-for-beginners-the-definitive-practical-guide)

**IPPC Repository:** <https://github.com/hypertexthero/ippcdj> - The master branch that should eventually be the same code that is live at production website. Another, likely better, option is to create an IPPC Organization page and move this there. 

## Data migrations using South app after changing models

Make sure 'south' is present in your INSTALLED_APPS IN settings.py.

If you add new fields or change certain values of existing ones such as blank or null in the ippc application, you need to do a data migration to synchronize the database:

1. If you followed the Installation / Setup steps above go to step 2. Otherwise run the following in the terminal:

        python manage.py convert_to_south ippc

2. Everytime you make a change in your models do the following:

        python manage.py schemamigration ippc --auto
        python manage.py migrate ippc

3. If you want to revert to a previous migration, look for the previous migration number in ippc/migrations and replace #### with the migration number in the following command:

        manage.py migrate your_app ####


## Translation updates for non-user-generated site content

<https://docs.djangoproject.com/en/dev/topics/i18n/translation/>

Edit the django.po file for each language in `ippcdj_repo/conf/locale/` and then run the following commands in the terminal to compile the translation files: 

    python manage.py makemessages --all
    python manage.py compilemessages

## Deployment

Dev server exlqaippc2.ext.fao.org setup and configuration for IPPC 4.0 prototype at <http://dev.ippc.int/en/> (only available within FAO network). To update code (eventually this will all be done with one command which fires a fabric script such as `fab deploy dev`):

1. ssh into dev server
2. change directory to ~/projects/ippcdj-env and activate virtualenv with `. bin/activate`
3. change directory to ~/projects/ippcdj-env/ippcdj_repo
4. pull changes `git pull`
5. move any static media to proper serving location `python manage.py collectstatic`
6. run any data migrations on the database:

        python manage.py schemamigration ippc --auto
        python  manage.py migrate ippc

7. Compile translations

        python manage.py makemessages --all
        python manage.py compilemessages

8. Kill [gunicorn](http://gunicorn-docs.readthedocs.org/en/latest/run.html) process `pkill gunicorn` then restart it `gunicorn_django --daemon -b 0.0.0.0:8000`
9. Stop nginx `service nginx stop` then restart `service nginx start`

## Example Nginx Configuration

    # phpmyadmin.site.tld (dev only to aid management of MySQL DB. Do not install in production.)
    server {
        listen xxx.xxx.x.xxx:80;
        server_name phpmyadmin.site.tld;
        
        root /path/to/phpmyadmin;
        index index.html index.php;
        
        location / {
                index index.html index.htm index.php;
            }
            
        location ~ \.php$ {
            expires    off;
            include /etc/nginx/fastcgi_params;
            fastcgi_pass    127.0.0.1:9000;
            fastcgi_index   index.php;
            fastcgi_param   SCRIPT_FILENAME  /path/to/phpmyadmin/$fastcgi_script_name;
        }
    }
    
    
    # dev.site.tld
    server {
      listen xxx.xxx.x.xxx:80;
      server_name dev.site.tld;
      access_log  /var/log/nginx/dev_site_tld.log;
      
      location /admin/media/ {
          # this changes depending on your python version
          root /path/to/env/lib/python2.7/site-packages/django/contrib;
      }
      
      location /static/media { # STATIC_URL
          alias /path/to/env/repo/static/media; # STATIC_ROOT
          expires 30d;
      }
      
      location /static { # STATIC_URL
          alias /path/to/env/repo/static; # STATIC_ROOT
          expires 30d;
      }
      
      location / {
          proxy_pass http://127.0.0.1:8000;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          }
          
      # what to serve if upstream is not available or crashes
      error_page 500 502 503 504 /media/50x.html;
    }

## MariaDB (MySQL)

For setup see <http://www.tecmint.com/install-mariadb-in-linux/>:

Start:

    /etc/init.d/mysql start

Login:

    

## Permissions System

- Implemented using [django-guardian](https://github.com/lukaszb/django-guardian)

**Server Architecture**

    Request ----> Reverse-Proxy Server (Nginx)
                     |
                      \                           
                       `-> App Server (Gunicorn). 127.0.0.1:8081 --> Django app

**Current Software Stack**

- [Python 2.7.6, Pip and Virtualenv](http://www.jeffknupp.com/blog/2013/12/18/starting-a-django-16-project-the-right-way/)[^1]
- [Nginx](http://wiki.nginx.org/Install) _web & reverse proxy server_
- [Gunicorn](https://www.digitalocean.com/community/articles/how-to-deploy-python-wsgi-apps-using-gunicorn-http-server-behind-nginx) _web application WSGI server_

The main web application is built with [Django](https://www.djangoproject.com/) and [Mezzanine](http://mezzanine.jupo.org).

