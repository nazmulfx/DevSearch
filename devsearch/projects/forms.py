from django.forms import ModelForm
from django import forms
from . models import Project, Review

class projectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link', 'tags']
        
        # Note: To customize form fields > from django import forms & work in widgets
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
        
    # Note: css class in input, 
    def __init__(self, *args, **kwargs):
        super(projectForm, self).__init__(*args, **kwargs)
        #Note: in for loop way
        for label, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
        
        #Note: Manually adding single by single
        # self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder': 'Add your text'})
        # self.fields['description'].widget.attrs.update({'class': 'input', 'placeholder': 'Add your text'})
        # self.fields['demo_link'].widget.attrs.update({'class': 'input', 'placeholder': 'Add your text'})
        # self.fields['source_link'].widget.attrs.update({'class': 'input', 'placeholder': 'Add your text'})  


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
        
        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        #Note: in for loop way
        for label, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})