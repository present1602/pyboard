from .models import Qna
from django import forms
from django.forms import Textarea


class QnaForm(forms.ModelForm):
    # text = forms.CharField(label="", widget=forms.TextArea(attrs={'cols':5, 'rows':3}))

    class Meta:
        model = Qna
        fields = ['text']
        widgets = {
            'text': Textarea(attrs={'cols':5,
                                    'rows':3,
                                    'placeholder': '내용을 입력해주세요',
                                    }
                             )
        }


