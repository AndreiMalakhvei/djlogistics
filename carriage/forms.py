from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from carriage.models import City, Warehouse

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



class WarehouseRequestForm(forms.Form):
    @staticmethod
    def date_limit():
        return date.today()

    pll_num = forms.IntegerField(label='Number of pallets', widget=forms.NumberInput(attrs={'class': "form-control myform-control check", 'autocomplete': "off"}))
    codes_num = forms.IntegerField(label='Number of customs codes', widget=forms.NumberInput(attrs={'class': "form-control myform-control check", 'autocomplete': "off"}))
    units_num = forms.IntegerField(label='Number of units for labelling', widget=forms.NumberInput(attrs={'class': "form-control myform-control check", 'autocomplete': "off"}))
    arr_date = forms.DateField(label='Date of arrival', validators=[MinValueValidator(date_limit)], widget=forms.DateInput(attrs={'type':'date', 'min': date_limit,
                                'class': "form-control myform-control check", 'autocomplete': "off"}))
    dep_date = forms.DateField(label='Date of departure', validators=[MinValueValidator(date_limit)],
                               widget=forms.DateInput(attrs={'type': 'date', 'min': date_limit,
                                'class': "form-control myform-control check", 'autocomplete': "off"}))

    t1 = forms.BooleanField(label='Cargo is under customs control procedure', required=False, widget=forms.CheckboxInput(attrs={'class': " ", 'type': "checkbox", 'value':"", 'id':"", 'autocomplete': "off"}))

    def clean(self):
        cleaned_data = super().clean()
        first_date = cleaned_data.get("arr_date")
        second_date = cleaned_data.get("dep_date")

        if second_date < first_date:
            raise ValidationError(
                "Departure can`t be earlier than arrival. Please check defined dates "
            )

