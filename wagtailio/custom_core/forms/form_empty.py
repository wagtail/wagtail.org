from django.forms import forms


# classes
class EmptyForm(forms.Form):
    class Meta:
        fields = []
