from django import forms
from pybo.models import question, answer


class questionForm(forms.ModelForm):
    class Meta:
        model = question  # 사용할 모델
        fields = ['subject', 'content']
        labels = {
            'subject': '제목',
            'content': '내용',
        }

class answerForm(forms.ModelForm):
  class Meta:
    model = answer
    fields = ['content']
    labels = {
      'content':'답변내용',
    }