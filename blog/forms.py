from django import forms
from .models import Blog
from ckeditor.widgets import CKEditorWidget

class BlogForm(forms.ModelForm):
    title = forms.CharField(max_length=200)
    
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Blog
        fields = ['content']



