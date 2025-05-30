from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, Skill #Edit profile, Skill form

# User-Registration form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2'] # if done proceed to the Users aps views registration
        labels = {
            'first_name': 'Name',
        }
          # This code design form input form
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})



# user-account edit form    
class ProfileForm(ModelForm):
        class Meta:
            model = Profile
            fields = ['name', 'email', 'username', 'location', 'bio', 'short_intro', 'profile_image', 'social_github', 
                      'social_linkedin', 'social_twitter', 'social_youtube', 'social_website' ]
            
        def __init__(self, *args, **kwargs):
         super(ProfileForm, self).__init__(*args, **kwargs)

         for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})



# Skill form
class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
         super(SkillForm, self).__init__(*args, **kwargs)

         for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
 
