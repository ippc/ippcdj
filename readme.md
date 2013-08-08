# Needed:

- [Pest Report mapping](http://leafletjs.com/examples/choropleth.html)
- Homepage design

- Publications list page
- [Calendar](https://github.com/shurik/mezzanine.calendar) (or [Events](https://github.com/stbarnabas/mezzanine-events)?)
- Forums
- Email utility
- Contact form
- Sitemap
- Use jQuery [multi-file-upload](https://github.com/sigurdga/django-jquery-file-upload) functionality for uploading images and files to be inserted in pages and blog posts, [with additional fields for each file](https://github.com/blueimp/jQuery-File-Upload/wiki/How-to-submit-additional-form-data) if required.
- Author field for publications
- Last modified date for pages and publications
- Versioning of all page content?
- [Download multiple files](http://stackoverflow.com/a/12951557/412329)
- Use [Chosen](http://harvesthq.github.io/chosen/) to make globalnav dropdowns friedly. Also in admin. There's a [Django app](https://github.com/theatlantic/django-chosen), too.
- Order permission groups alphabetically in admin
- Country pages:
    - Versioning of Pest Reports. Report number: GBR-32/1. When edited: GBR-32/2.
    - Other country forms
    - Prevent hidden report titles from appearing in search results
    - Country RSS feeds
- User registration open but behind login-required and super-user required so only admins can add new users, who get notification emails to confirm account and set own password. OR, user registration open to all, but need approval by admins.
