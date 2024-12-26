from django.forms import ModelForm, widgets
from .models import Project
from django import forms


# Create project form
class projectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'featured_image', 'demo_link', 'source_link',  'tags']
        #Checkbox design
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
    # This code design form input form
    def __init__(self, *args, **kwargs):
        super(projectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


    