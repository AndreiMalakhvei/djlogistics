from django import forms

from carriage.models import City

class MyTextInput(forms.TextInput):
    class Media:
        css = {
            'all': ('carriage/base_css/mycss.css',)
        }



class TestForm(forms.Form):
    test_field = forms.CharField(widget=MyTextInput)
    from_city = forms.ModelChoiceField(label='from city', queryset=City.objects.all(),
                                       widget=forms.Select(attrs={'class': "form-select form-select-lg mb-3 custom"}))
    to_city = forms.ModelChoiceField(label='to city', queryset=City.objects.all(),
                                     widget=forms.Select(attrs={'class': "form-select form-select-lg mb-3"}))
    selection_list = [(1, 'Time'), (2, 'Price')]
    selection = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'form-check-input', 'type': 'radio', 'name': 'flexRadioDefault',
                                                                  'id': 'flexCheckDefault'}), label='Priority',
                                  choices=selection_list)




class TestDisplayForm(forms.Form):
    from_city = forms.CharField(label='City of Departure')
    to_city = forms.CharField(label='City of Destination')
    transit_time = forms.FloatField(label='Transit Time')
    price = forms.FloatField(label='Price')
    details = forms.CharField(label='Detailed Route')


