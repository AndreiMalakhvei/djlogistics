from django import forms

from carriage.models import City


class TestForm(forms.Form):
    from_city = forms.ModelChoiceField(label='from city', queryset = City.objects.all(), widget=forms.Select)
    to_city = forms.ModelChoiceField(label='to city', queryset=City.objects.all(), widget=forms.Select)
    selection_list = [(1, 'Time'), (2, 'Price')]
    selection = forms.ChoiceField(widget=forms.RadioSelect(), label='priority', choices=selection_list)



class TestDisplayForm(forms.Form):
    from_city = forms.CharField(label='City of Departure')
    to_city = forms.CharField(label='City of Destination')
    transit_time = forms.FloatField(label='Transit Time')
    price = forms.FloatField(label='Price')
    details = forms.CharField(label='Detailed Route')