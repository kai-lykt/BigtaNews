from django import forms
from .models import Article
from django_summernote.widgets import SummernoteWidget


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': '_174'}),
            'content': SummernoteWidget(attrs={
                'summernote': {
                    'width': '979px',
                    'height': '450px'
                }
            }),
        }
