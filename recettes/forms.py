from django import forms
from .models import Recettes, RecetteComment

class CommentForm(forms.ModelForm):
    class Meta:
        model = RecetteComment
        fields = ('comment',)