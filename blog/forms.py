from django import forms

    

from tinymce.widgets import TinyMCE
from tinymce import models as tinymce_models
from .models import Blog, BlogComment, Likes
from django.core.exceptions import ValidationError


class TinyMCEWidget(TinyMCE): 
    def use_required_attribute(self, *args): 
        return False


class BlogForm(forms.ModelForm):
    blog_title = forms.CharField(required=True, label="", widget=forms.TextInput(attrs={'placeholder':'Titre de l\'article'}))
    blog_content = forms.CharField(widget=TinyMCEWidget(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Blog
        # fields = ['blog_title', 'blog_content', 'blog_image']
        fields = '__all__'


    def clean_photo(self):
         blog_image = self.cleaned_data.get('blog_image',None)
         if not blog_image:
             raise ValidationError("Something went wrong")
         if blog_image._height < 200 or blog_image._width < 200:
             raise ValidationError("Photo dimensions are too small (minimum 200X200 )")

         return blog_image

# class BlogForm(forms.ModelForm):
#      def clean_photo(self):
#          blog_image = self.cleaned_data.get('blog_image',None)
#          if not blog_image:
#              raise ValidationError("Something went wrong")
#          if blog_image._height < 200 or blog_image._width < 200:
#              raise ValidationError("Photo dimensions are too small (minimum 200X200 )")

#          return blog_image

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = BlogComment
        fields = ("comment",)
