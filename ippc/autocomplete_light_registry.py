import autocomplete_light

from .models import EppoCodes, IssueKeywords, CommodityKeywords


autocomplete_light.register(EppoCodes, search_fields=('codename',),
               autocomplete_js_attributes={'placeholder': '....'})
autocomplete_light.register(IssueKeywords, search_fields=('name',),
               autocomplete_js_attributes={'placeholder': '....'})
autocomplete_light.register(CommodityKeywords, search_fields=('name',),
               autocomplete_js_attributes={'placeholder': '....'})
