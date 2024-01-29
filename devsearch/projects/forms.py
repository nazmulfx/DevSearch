from django.forms import ModelForm
from . models import Project

class projectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'