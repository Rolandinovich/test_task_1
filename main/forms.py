from django import forms
from main.models import Recruit, Answer


class RecruitForm(forms.ModelForm):
    '''Форма для создания рекрута'''
    class Meta:
        model = Recruit
        fields = ('name', 'planet', 'age', 'email')


class RecruitTestForm(forms.ModelForm):
    '''Форма для генерации списка вопросов теста'''
    class Meta:
        model = Answer
        fields = ('question', 'answer')

    def __init__(self, *args, **kwargs):
        super(RecruitTestForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['question'].widget.attrs['hidden'] = True
