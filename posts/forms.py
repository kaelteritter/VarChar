from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.TextInput(
            attrs={
        'class': 'form-control me-2',
        'placeholder': "Напишите комментарий",
        'rows': 1
    }
    )
    )
    class Meta:
        model = Comment
        fields = ['text']