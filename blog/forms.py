from django import forms
from .models import Post, Comment

class EmailPostForm(forms.Form):
    name=forms.CharField(max_length=250)
    email=forms.EmailField()
    to=forms.EmailField()
    comment=forms.CharField(widget=forms.Textarea, required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')

class SerachForm(forms.Form):
    query = forms.CharField()