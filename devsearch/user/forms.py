from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . models import Profile, Skill


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
        }
        
        # Note: css class in input, 
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        #Note: in for loop way
        for label, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        #fields = '__all__'
        #exclude = ['user']
        fields = ['name', 'email', 'username', 'location', 'short_intro', 'bio', 'profile_pic', 'social_github', 'social_twitter', 'social_linkedin', 'social_youtube', 'social_facebook']
        labels = {
            'social_github': 'Github',
            'social_twitter': 'Twitter',
            'social_linkedin': 'Linkedin',
            'social_youtube': 'Youtube',
            'social_facebook': 'Facebook',
        }
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        for label, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
            
            
class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']
    
    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        
        for label, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})