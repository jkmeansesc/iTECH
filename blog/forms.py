from django import forms
from .models import Blog
from ckeditor.widgets import CKEditorWidget


class BlogForm(forms.ModelForm):
    title = forms.CharField(max_length=200, label='Title')
    tag = forms.CharField(max_length=200, label='Tag')
    content = forms.CharField(widget=CKEditorWidget())
    # comment_num = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    image = forms.ImageField(label='Image', required=False)

    class Meta:
        model = Blog
        fields = ['title', 'tag', 'content', 'image']



# class CommentForm(forms.ModelForm):
#     content = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Add a comment...'}))
#
#     class Meta:
#         model = Comment
#         fields = ['content']
