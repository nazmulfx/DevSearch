from django.forms import ModelForm
from django import forms
from . models import Project

class projectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link', 'tags']
        
        # Note: To customize form fields > from django import forms & work in widgets
        widgets = {
            'tags': forms.CheckboxSelectMultiple()
        }
        
        # Note: css class in input, 
        def __init__(self, *args, **kwargs):
            super(projectForm, self).__init__(*args, **kwargs)
            #Note: in for loop way
            for name, field in self.fields.item():
                field.widget.attrs.update({'class':'input'})
            
            #Note: Manually adding single by single
            # self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder': 'Add your text'})
            # self.fields['description'].widget.attrs.update({'class': 'input', 'placeholder': 'Add your text'})
            # self.fields['demo_link'].widget.attrs.update({'class': 'input', 'placeholder': 'Add your text'})
            # self.fields['source_link'].widget.attrs.update({'class': 'input', 'placeholder': 'Add your text'})