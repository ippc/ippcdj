# Better content management system for IPPC

Based on [Django](https://www.djangoproject.com/) and [Mezzanine](http://mezzanine.jupo.org).

Here's [some documentation to get started](https://github.com/hypertexthero/ippcdj/blob/master/docs/documentation.md).

## Things to do

- Setup IPPC GitHub account and [IPPC Web Development Workflow](http://it.ippc.int/posts/Simon/795-ippc-web-development-workflow/) and test with [Paola](https://github.com/psentinelli)
- Fix file upload in [Country Pest Report upload form](https://github.com/hypertexthero/ippcdj/blob/master/ippc/views.py#L142)
- Country pages:
    - Versioning of Pest Reports. Report number: GBR-32/1. When edited: GBR-32/2.
    - Other country forms
    - Prevent hidden report titles from appearing in search results
    - Country RSS feeds
- Author field for publications
- Create separate User database to be used by all IPPC-related apps for authentication
    - Users
        - Email
        - Password
        - First Name
        - Last Name
    - IPPC (profile in each web app extends above Users DB authentication defaults)
        - User(Fk to Users)
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
- User registration open but behind login-required and super-user required so only admins can add new users, who get notification emails to confirm account and set own password. OR, user registration open to all, but need approval by admins. i.e. Account registration & [activation](http://mezzanine.jupo.org/docs/user-accounts.html#account-approval) system?
- [Email utility](https://github.com/pinax/django-mailer)
    - Ability to insert user groups as well as individual users in `To:` field in `/admin/mailer/message/add/`
        - Use [admin actions](https://docs.djangoproject.com/en/1.5/ref/contrib/admin/actions/)?
        - [Custom admin form](http://stackoverflow.com/a/6099360/412329) overriding mailer's default form? Also see [this](http://djangosnippets.org/snippets/1650/) and [this](https://gist.github.com/luzfcb/1712348)
        - Custom email utility app and admin form calling django-mailer and groups?
- Homepage design
    - ¿'Add Pest Report' button in countries for NPPOs, visible even when user is logged out. Once user logs in, if they're an NPPO, they are redirected to the pest report form for their country?
- [Calendar](https://github.com/shurik/mezzanine.calendar) (or [Events](https://github.com/stbarnabas/mezzanine-events)?)
- Forums
- Contact form
- FAQ
- Last modified date for pages
- Use jQuery [multi-file-upload](https://github.com/sigurdga/django-jquery-file-upload) functionality for uploading images and files to be inserted in pages and blog posts, [with additional fields for each file](https://github.com/blueimp/jQuery-File-Upload/wiki/How-to-submit-additional-form-data) if required.
- Order permission groups alphabetically in admin
- Versioning of all page content?
- [Pest Report mapping](http://leafletjs.com/examples/choropleth.html)
    - <http://blog.thematicmapping.org/2008/04/thematic-mapping-with-geojson.html>
    - <http://blog.thematicmapping.org/2012/11/how-to-minify-geojson-files.html>
    - Examples:
        - [Geochart](https://developers.google.com/chart/interactive/docs/gallery/geochart)
        - [Income levels example](http://humangeo.github.io/leaflet-dvf/examples/html/incomelevels.html)
        - [Top Cities](http://techslides.com/leaflet-map-with-utfgrid-and-php-served-mbtiles/)
- [Download multiple files](http://stackoverflow.com/a/12951557/412329)
- Use [Chosen](http://harvesthq.github.io/chosen/) to make globalnav dropdowns friedly. Also in admin. There's a [Django app](https://github.com/theatlantic/django-chosen), too.