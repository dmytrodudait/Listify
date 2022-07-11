from django.forms import ModelForm
from .models import Listify

class ListifyForm(ModelForm):
    class Meta:
        model = Listify
        fields = ['title', 'memo', 'important']
 