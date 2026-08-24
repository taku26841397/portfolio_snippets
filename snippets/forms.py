from django import forms
from .models import ImagePrompt

class ImagePromptForm(forms.ModelForm):
    class Meta:
        model =ImagePrompt
        
        fields =['title','prompt','base_image','generated_image','language']