import autocomplete_light

from .models import EppoCode, IssueKeyword, CommodityKeyword#,TestKeyword


autocomplete_light.register(EppoCode, search_fields=('codename',),
               autocomplete_js_attributes={'placeholder': '....'})
autocomplete_light.register(IssueKeyword, search_fields=('name',),
               autocomplete_js_attributes={'placeholder': '....'})
autocomplete_light.register(CommodityKeyword, search_fields=('name',),
               autocomplete_js_attributes={'placeholder': '....'})
#autocomplete_light.register(TestKeyword, search_fields=('name',),
#               autocomplete_js_attributes={'placeholder': '....'})
               