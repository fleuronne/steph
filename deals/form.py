from django import forms


# creating a form
class InputForm(forms.Form):
    choices = ((0, 0), (1, 1), (2, 2), (3, 3))
    choicesd = ( (0, 0), (1, 1), (2, 2), (3, 3))
    choicesms = ( (0, 0), (1, 1), (2, 2), (3, 3))
    days_choices = ((1, 1), (3, 3), (7, 7), (30, 30))
    price = forms.CharField(max_length=200, required=True)
    data = forms.ChoiceField(choices=choices, initial=3)
    call = forms.ChoiceField(choices=choices, initial=0)
    sms = forms.ChoiceField(choices=choicesms, initial=0)
    days = forms.ChoiceField(choices=days_choices, initial=1)

    class Meta:
        fields = ["price", "data", "call", "sms", "days"]
        def __init__(self, *args, **kwargs):
            super(InputForm, self).__init__(*args, **kwargs)
            self.fields["price"].widget.attrs.update(
                {'class': 'form-control', 'placeholder': 'Enter your price'}
            )
            self.fields["data"].widget.attrs.update(
                {'class': 'form-control', 'placeholder': 'Choose a priority'}
            )
            self.fields["sms"].widget.attrs.update(
                {'class': 'form-control', 'placeholder': 'Choose a priority'}
            )
            self.fields["call"].widget.attrs.update(
                {'class': 'form-control', 'placeholder': 'Choose a priority'}
            )
            self.fields["days"].widget.attrs.update(
                {'class': 'days', 'placeholder': 'Choose a number of date'}
            )
