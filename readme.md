# IPPC 4.0

## Things to do

- FAQ update
- User registration open but behind login-required and staff-user required. The URL to add new users is `/account/signup/`
- Add blog and forum category management page to admin: 
    - http://127.0.0.1:8000/en/admin/blog/blogcategory/
    - http://127.0.0.1:8000/en/admin/forum/forumcategory/
- Eventually update to Mezzanine 3.1.5
    - Update to latest version of Mezzanine and make sure current functionality works
- Document nginx/gunicorn/supervisor setup (currently running gunicorn with deprecated `gunicorn_django -b 0.0.0.0:8000` command — get it running and working with recommended command instead)
- Last modified date for pages
- The All Our Users Database. Two options:
    1. Create[Single Sign-On](https://docs.djangoproject.com/en/1.5/topics/auth/customizing/) (see also [this](https://meta.discourse.org/t/sso-example-for-django/14258) and [this](https://github.com/Bouke/django-federated-login/tree/master/example)) and **[this](https://gist.github.com/kenbolton/4946936)** - a separate Accounts database to be used by all IPPC-related apps for authentication and authorization. The database should contain two tables:
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
    2. [All websites run off the same application instance](http://stackoverflow.com/questions/1581602/django-sharing-authentication-across-two-sites-that-are-on-different-domains) with [custom authentication backend](http://stackoverflow.com/questions/1404131/how-to-get-unique-users-across-multiple-django-sites-powered-by-the-sites-fram)
- [IRSS](https://github.com/ASKBOT/askbot-devel) refactor
    - The easiest way to implement this is probably to use [CAS-Provider and CAS-consumer](http://stackoverflow.com/a/4663223) or [django-cas](https://bitbucket.org/cpcc/django-cas/overview). Another option: [mama-cas](https://github.com/jbittel/django-mama-cas). Relevant documentation pages: [multiple databases](https://docs.djangoproject.com/en/1.5/topics/db/multi-db/), [authentication](https://docs.djangoproject.com/en/1.5/topics/auth/customizing/), [multiple sites framework](https://docs.djangoproject.com/en/1.5/ref/contrib/sites/). See also [this blog post](http://reinout.vanrees.org/weblog/2014/05/09/authentication-python-web.html).
- Phytosanitary.info refactor (use [original code](https://github.com/hypertexthero/phytosanitary)?)
- Both phytosantiary.info and apppc.org will need to get SSL certificates for single sign-on to work securely: 
        > Even if the authentication with CAS is made using a mechanism which makes it difficult to interfere with, all authorized communication will subsequentely use a cookie identifing the session which can be used to hijack the connection. So you need to encrypt the communication. There is just no way around that if you want to enforce some sort of security.
- Order permission groups alphabetically in admin
- Setup working fabric script for easy deployment that does the following after running `fab deploy dev`:
    1. Adds, commits and pushes files to Github (for future: if tests pass)
    2. Logs in to dev.ippc.int, activates application virtualenv and pulls changes from Github
    3. Collect static files to locations to be served on dev server
    4. Restart gunicorn and nginx 
- If no publication or agenda numbers exist, don't show header or cells
- [Versioning](https://django-simple-history.readthedocs.org/en/latest/) of all page content?
- [wiki.ippc.int](http://www.nomachetejuggling.com/2012/05/15/personal-wiki-using-github-and-gollum-on-os-x/)

## Installation / Setup


1. Install Django development environment on your computer and follow instructions to get it running: <http://wiki.bitnami.com/Infrastructure_Stacks/BitNami_Django_Stack>

2. Clone code repository (currently on GitHub), move into it and install third-party libraries for the project:

    ````
    git clone https://github.com/hypertexthero/ippcdj.git ippcdj_repo
    cd ippcdj_repo
    pip2.7 install -r requirements/project.txt
    mv local_settings_example.py local_settings.py 
    python manage.py createdb
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
    cd ~/projects
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


If you mess up or want an overview to understand what south is doing, see [here](http://stackoverflow.com/a/4840262)

## Translation updates for non-user-generated site content

<https://docs.djangoproject.com/en/dev/topics/i18n/translation/>

Edit the django.po file for each language in `ippcdj_repo/conf/locale/` and then run the following commands in the terminal to compile the translation files: 

    python manage.py makemessages --all
    python manage.py compilemessages

## Deployment & Data Migrations

Dev server exlqaippc2.ext.fao.org setup and configuration for IPPC 4.0 prototype at <http://dev.ippc.int/en/> (only available within FAO network). To update code (eventually this will all be done with one command which fires a fabric script such as `fab deploy dev`):


1. ssh root@hqldvippc2.hq.un.fao.org

		ssh root@hqldvippc2.hq.un.fao.org

2. Change directory to the project and activate virtualenv

		cd /work/projects/ippcdj-env && . bin/activate

3. Change to repository directory

		cd	ippcdj_repo/

4. Pull latest changes. If you get a warning about overwriting existing changes, do `git stash save --keep-index` then `git stash drop` <http://stackoverflow.com/a/14318266>

		git pull

5. <del>move any static media to proper serving location `python manage.py collectstatic`</del> Not necessary anymore as we have configured nginx to look in the right places for static media.

6. <del>Run any data migrations on the database:</del> Right now we're just transfering the whole dump from dev to the MySQL server when models are updated. 

        python manage.py schemamigration ippc --auto
        python  manage.py migrate ippc

7. Compile and make translations 

		python manage.py makemessages --all
		python manage.py compilemessages

8. Stop and restart [Gunicorn](http://gunicorn-docs.readthedocs.org/en/latest/run.html) application server (todo: find way to do this gracefully, so existing processes, such as a user submitting a form, don't fail:

		pkill gunicorn
		gunicorn_django --daemon -b 0.0.0.0:8000

9. Restart Nginx reverse-proxy server (web-facing) server

		service nginx restart


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

[MySQL](http://www.tecmint.com/install-mariadb-in-linux/), [php](http://www.if-not-true-then-false.com/2011/install-nginx-php-fpm-on-fedora-centos-red-hat-rhel/) and [phpmyadmin](http://stackoverflow.com/questions/5895707/how-to-combine-django-and-wordpress-based-on-ubuntu-and-nginx)

Start:

    /etc/init.d/mysql start


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

