from django import forms
from django.core.exceptions import ValidationError

from carriage.models import City

class MyTextInput(forms.TextInput):
    class Media:
        css = {
            'all': ('carriage/base_css/mycss.css',)
        }



class RouteFindForm(forms.Form):
    form_qs = City.objects.select_related().order_by('country__name', 'name')
    list_of_cities = [(i.name, ", ".join((str(i.country.name), str(i.name)))) for i in form_qs]

    # test_field = forms.CharField(widget=MyTextInput)
    from_city = forms.ChoiceField(label='from city', choices=list_of_cities,
                                 widget=forms.Select(attrs={'class': "form-select form-select-lg mb-3 custom"}))
    to_city = forms.ChoiceField(label='to city', choices=list_of_cities,
                                     widget=forms.Select(attrs={'class': "form-select form-select-lg mb-3"}))
    selection_list = [(1, 'Time'), (2, 'Price')]
    selection = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'form-check-input', 'type': 'radio', 'name': 'flexRadioDefault',
                                                                  'id': 'flexCheckDefault'}), label='Priority',
                                  choices=selection_list)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     to_city = cleaned_data.get("to_city")
    #     from_city = cleaned_data.get("from_city")
    #
    #     if to_city == from_city:
    #         # msg = "Cities of departure and destination must be different"
    #         # self.add_error('to_city', msg)
    #         # self.add_error('from_city', msg)
    #         raise ValidationError(
    #             "Cities of departure and destination must be different "
    #             "CC'ing yourself."
    #         )


class TestDisplayForm(forms.Form):
    from_city = forms.CharField(label='City of Departure')
    to_city = forms.CharField(label='City of Destination')
    transit_time = forms.FloatField(label='Transit Time')
    price = forms.FloatField(label='Price')
    details = forms.CharField(label='Detailed Route')


