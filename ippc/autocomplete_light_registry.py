import autocomplete_light

from .models import EppoCode, IssueKeyword, CommodityKeyword, PhytosanitaryTreatmentType, Topic
from django.contrib.auth.models import User
from t_eppo.models import Names


autocomplete_light.register(EppoCode, search_fields=('codename',),
               autocomplete_js_attributes={'placeholder': '....'})
autocomplete_light.register(Names, search_fields=('codename',),
               autocomplete_js_attributes={'placeholder': '....',})
autocomplete_light.register(IssueKeyword, search_fields=('name',),
               autocomplete_js_attributes={'placeholder': '....'})
autocomplete_light.register(CommodityKeyword, search_fields=('name',),
               autocomplete_js_attributes={'placeholder': '....'})
autocomplete_light.register(PhytosanitaryTreatmentType, search_fields=('typefullname',),
               autocomplete_js_attributes={'placeholder': '....'})
autocomplete_light.register(User, search_fields=('first_name','last_name'),
               autocomplete_js_attributes={'placeholder': '....'})
autocomplete_light.register(Topic, search_fields=('topicnumber',),choices=Topic.objects.filter(is_version=False),
               autocomplete_js_attributes={'placeholder': '....'})
 