# Better content management system for IPPC

Based on [Django](https://www.djangoproject.com/) and [Mezzanine](http://mezzanine.jupo.org).

# Todo:

- Ability to authenticate against external user database
    - [Identity Authentication on the Internet](http://hypertexthero.com/logbook/2013/08/identity-internet/)
    - [Drupal 7 password hasher for Django](http://stackoverflow.com/q/9876700/412329)
- [Pest Report mapping](http://leafletjs.com/examples/choropleth.html)
    - <http://blog.thematicmapping.org/2008/04/thematic-mapping-with-geojson.html>
    - <http://blog.thematicmapping.org/2012/11/how-to-minify-geojson-files.html>
    - Examples:
        - [Geochart](https://developers.google.com/chart/interactive/docs/gallery/geochart)
        - [Income levels example](http://humangeo.github.io/leaflet-dvf/examples/html/incomelevels.html)
        - [Top Cities](http://techslides.com/leaflet-map-with-utfgrid-and-php-served-mbtiles/)
- Homepage design
- Email utility
- [Calendar](https://github.com/shurik/mezzanine.calendar) (or [Events](https://github.com/stbarnabas/mezzanine-events)?)
- Forums
- Contact form
- FAQ
- Sitemap
- Author field for publications
- Versioning of all page content?
- Country pages:
    - Versioning of Pest Reports. Report number: GBR-32/1. When edited: GBR-32/2.
    - Other country forms
    - Prevent hidden report titles from appearing in search results
    - Country RSS feeds
- Last modified date for pages
- Use jQuery [multi-file-upload](https://github.com/sigurdga/django-jquery-file-upload) functionality for uploading images and files to be inserted in pages and blog posts, [with additional fields for each file](https://github.com/blueimp/jQuery-File-Upload/wiki/How-to-submit-additional-form-data) if required.
- [Download multiple files](http://stackoverflow.com/a/12951557/412329)
- Use [Chosen](http://harvesthq.github.io/chosen/) to make globalnav dropdowns friedly. Also in admin. There's a [Django app](https://github.com/theatlantic/django-chosen), too.
- Order permission groups alphabetically in admin
- User registration open but behind login-required and super-user required so only admins can add new users, who get notification emails to confirm account and set own password. OR, user registration open to all, but need approval by admins.
