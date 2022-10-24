from django import forms
from django.core.exceptions import ValidationError

from carriage.models import City

class RouteFindForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # add custom error messages
        self.fields['to_city'].error_messages.update({
            'required': 'Please let us know what to call you!',
        })


    form_qs = City.objects.select_related().order_by('country__name', 'name')
    list_of_cities = [(i.name, ", ".join((str(i.country.name), str(i.name)))) for i in form_qs]

    # test_field = forms.CharField(widget=MyTextInput)
    from_city = forms.ChoiceField(label='from city', choices=list_of_cities,
                                 widget=forms.Select(attrs={'class': "form-select form-select-lg mb-3 "}))
    to_city = forms.ChoiceField(label='to city', choices=list_of_cities,
                                     widget=forms.Select(attrs={'class': "form-select form-select-lg mb-3"}))
    selection_list = [(1, 'Time as Priority'), (2, 'Price as Priority')]
    selection = forms.ChoiceField(widget=forms.RadioSelect(), label='Priority',  choices=selection_list)
    # error_messages = {
    #     'to_city': {
    #         'required': "This writer's name is too long."
    #     }}

    def clean(self):
        cleaned_data = super().clean()
        to_city = cleaned_data.get("to_city")
        from_city = cleaned_data.get("from_city")

        if to_city == from_city:
            # raise RouteFindForm.error_messages['to_city']
            # raise forms.ValidationError('ijbnrisgnngirnbignbihr')
            # raise RouteFindForm.to_city.error_messages['required']

            raise ValidationError(
                "Cities of departure and destination must be different "
            )


class TestDisplayForm(forms.Form):
    from_city = forms.CharField(label='City of Departure')
    to_city = forms.CharField(label='City of Destination')
    transit_time = forms.FloatField(label='Transit Time')
    price = forms.FloatField(label='Price')
    details = forms.CharField(label='Detailed Route')


class ContactForm(forms.Form):
    fname = forms.CharField(label='First Name', max_length=60, widget=forms.TextInput(attrs={'class': "form-control myform-control", 'autocomplete': "off"}))
    mail = forms.EmailField(label='email', widget=forms.TextInput(attrs={'class': "form-control myform-control", 'autocomplete':"off"}))
    phone = forms.CharField(label='Phone number', max_length=20, widget=forms.TextInput(attrs={'class': "form-control myform-control", 'autocomplete': "off"}))
    subject = forms.CharField(label='Subject', max_length=60, widget=forms.TextInput(attrs={'class': "form-control myform-control", 'autocomplete': "off"}))
    body = forms.CharField(label='Message', max_length=500, widget=forms.Textarea(attrs={'class': "form-control myform-control", 'autocomplete': "off"}))



