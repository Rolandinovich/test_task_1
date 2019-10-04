from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from main.forms import RecruitForm, RecruitTestForm
from main.models import TestTrial, Answer, Recruit, Sith


def start_page(request):
    return render(request, 'main/index.html', {'title': 'Рекрутинг ***Добро пожаловать***'})


def recruit_create(request):
    recruit = RecruitForm(data=request.POST or None)
    if request.method == 'POST' and recruit.is_valid():
        recruit.save()
        # создаю тестовые вопросы
        # так как о разных тестах речи не шло, беру из базы единственный
        test = TestTrial.objects.all().first()
        for question in test.questions.all():
            answer = Answer(recruit_id=recruit.instance.id, question=question)
            answer.save()
        return HttpResponseRedirect(reverse('main:recruit_test', args=[recruit.instance.id]))
    content = {'recruit_form': RecruitForm() if not recruit else recruit}
    return render(request, 'main/create_recruit.html', content)


class RecruitTest(UpdateView):
    model = Recruit
    fields = []
    success_url = reverse_lazy('main:finish_test')
    template_name = 'main/recruit_test.html'

    def get_context_data(self, **kwargs):
        data = super(RecruitTest, self).get_context_data(**kwargs)
        TestFormSet = inlineformset_factory(Recruit, Answer,
                                             form=RecruitTestForm, extra=0)
        if self.request.POST:
            data['test_form'] = TestFormSet(self.request.POST, instance=self.object)
        else:
            formset = TestFormSet(instance=self.object)
            data['test_form'] = formset

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        test_form = context['test_form']

        with transaction.atomic():
            self.object = form.save()
            if test_form.is_valid():
                test_form.instance = self.object
                test_form.save()
        return super(RecruitTest, self).form_valid(form)

def finish_test(request):
    return render(request, 'main/test_finish.html', {'title': 'Тестирование завершено. Ваши ответы приняты!'})

def sith_list(request):
    content = {'title':'Выбирите себя из списка',
               'siths':Sith.objects.all()}
    return render(request, 'main/sith_list.html', content)