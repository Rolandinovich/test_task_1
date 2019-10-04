from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView
from main.forms import RecruitForm, RecruitTestForm
from main.models import TestTrial, Answer, Recruit, Sith
from django.core.mail import send_mail


# Create your views here.

def start_page(request):
    '''Стартовый страница'''
    return render(request, 'main/index.html', {'title': 'Рекрутинг ***Добро пожаловать***'})


def recruit_create(request):
    ''' Создание рекрута и вопросов теста для него'''
    recruit = RecruitForm(data=request.POST or None)
    if request.method == 'POST' and recruit.is_valid():
        recruit.save()
        # создаю тестовые вопросы
        # так как о разных тестах речи не шло, беру из базы единственный тест
        test = TestTrial.objects.all().first()
        for question in test.questions.all():
            answer = Answer(recruit_id=recruit.instance.id, question=question)
            answer.save()
        return HttpResponseRedirect(reverse('main:recruit_test', args=[recruit.instance.id]))
    content = {'recruit_form': RecruitForm() if not recruit else recruit}
    return render(request, 'main/create_recruit.html', content)


class RecruitTest(UpdateView):
    '''Реализует получение ответов на вопросы теста'''
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
    '''Выводит страницу после завершения теста'''
    return render(request, 'main/test_finish.html', {'title': 'Тестирование завершено. Ваши ответы приняты!'})


def sith_list(request):
    '''Выводит список Ситхов'''
    content = {'title': 'Выбирите себя из списка',
               'siths': Sith.objects.all()}
    return render(request, 'main/sith_list.html', content)


def sith_detail(request, pk):
    ''' Выводит список всех рекрутов у Ситха'''
    try:
        sith = Sith.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return render(request, 'main/error_page.html')
    shadow_hadns = sith.recruits.all()
    shadow_hadns_count = shadow_hadns.count()
    recruits = Recruit.objects.all().exclude(pk__in=shadow_hadns.values_list('pk'))
    content = {
        'sith': sith,
        'shadow_hadns': shadow_hadns,
        'shadow_hadns_count': shadow_hadns_count,
        'recruits': recruits,
        'title': f'Рекруты ситха "{sith.name}"'
    }
    return render(request, 'main/sith_detail.html', content)


def add_recruit(request, pk_sith, pk_recruit):
    '''Добавляет рекрута Ситху'''
    try:
        sith = Sith.objects.get(pk=pk_sith)
        recruit = Recruit.objects.get(pk=pk_recruit)
    except ObjectDoesNotExist:
        return render(request, 'main/error_page.html')
    sith.recruits.add(recruit)
    send_mail(
        'Вас приняли в Руки Теней',
        f'{sith.name} принял Вас в Руки Теней',
        'recruting@mail.com',
        [recruit.email],
        fail_silently=True,
    )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def del_recruit(request, pk_sith, pk_recruit):
    '''Удаляет рекрута у Ситха'''
    try:
        sith = Sith.objects.get(pk=pk_sith)
        recruit = Recruit.objects.get(pk=pk_recruit)
    except ObjectDoesNotExist:
        return render(request, 'main/error_page.html')
    sith.recruits.remove(recruit)
    send_mail(
        'Вас исключили из Рук Теней',
        f'{sith.name} исключил Вас из Рук Теней',
        'recruting@mail.com',
        [recruit.email],
        fail_silently=True,
    )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def recruit_test_result(request, pk):
    '''Выводит страницу с результатами тестирования'''
    try:
        recruit = Recruit.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return render(request, 'main/error_page.html')
    answers = recruit.recruit_answers.all()
    content = {
        'answers': answers,
        'title': f'Ответы рекрута "{recruit.name}"',
        'next': request.META.get('HTTP_REFERER')
    }
    return render(request, 'main/show_test_result.html', content)
