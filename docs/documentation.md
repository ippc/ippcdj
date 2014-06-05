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

GitHub accounts are for codebase repository. Copies of codebase repository are also available in: 

1. Each developer's computer
2. dev.ippc.int server
3. ippc.int server

[**Fork & Pull Model** or **Shared Repository** model](https://help.github.com/articles/what-is-a-good-git-workflow)?

## GitHub Flow (how to work on www.ippc.int code):

1. [Fork Hypertexthero GitHub repository into own GitHub account, then clone it into your computer and add the original as upstream remote](https://help.github.com/articles/fork-a-repo):

2. To work on something new, [create a descriptively named branch](http://git-scm.com/book/en/Git-Branching-Basic-Branching-and-Merging) off of master (ie: iss53 - to resolve an example [issue](https://guides.github.com/features/issues/) #53).

        :::bash
        git checkout -b iss53

3. Commit to that branch locally and regularly push your work to the same named branch on your account.

        :::bash
        git commit -a -m 'fixed [issue 53]'
        git push origin

4. When you need feedback or help, or you think the branch is ready for merging, [open a pull request](https://help.github.com/articles/using-pull-requests).

5. After someone else has reviewed and signed off on the feature, you can merge it into master.

        git merge iss53
        git push upstream

If there's a conflict (two people edited the same lines on a file in a different way), you [can resolve it](http://git-scm.com/book/en/Git-Branching-Basic-Branching-and-Merging#Basic-Merge-Conflicts). 

6. Once it is merged and pushed to ‘master’, you can and should deploy immediately to dev/production server, either using a Fabric script to push to dev.ippc.int or www.ippc.int. Example: `fab push dev` or `fab push prod`, or a continuous integration server setup such as Jenkins (ideal — I don't know how to set this up yet), or manually logging into prod/dev server repo and doing a `git pull`.  

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
