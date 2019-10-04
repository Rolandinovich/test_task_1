from django.db import models


# Create your models here.
class Planet(models.Model):
    ''' Планета '''
    name = models.CharField('Название планеты', max_length=100)

    def __str__(self):
        return self.name


class Recruit(models.Model):
    ''' Рекрут '''
    name = models.CharField('Имя', max_length=100)
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE, verbose_name='Название планеты')
    age = models.PositiveIntegerField('Возраст')
    email = models.EmailField('Email', max_length=100)

    def __str__(self):
        return self.name


class Sith(models.Model):
    ''' Ситх '''
    name = models.CharField('Имя', max_length=100)
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE)
    recruits = models.ManyToManyField(Recruit, verbose_name='Рекруты этого Ситха', null=True, blank=True)

    def __str__(self):
        return self.name


class QuestionsList(models.Model):
    title = models.CharField('Текст вопроса', max_length=200)

    def __str__(self):
        return self.title


class TestTrial(models.Model):
    '''Тестовые испытания'''
    orden_code = models.CharField('Код ордена', max_length=50)
    questions = models.ManyToManyField(QuestionsList)

    def __str__(self):
        return self.orden_code


class Answer(models.Model):
    '''Ответы рекрута'''
    recruit = models.ForeignKey(Recruit, verbose_name='Рекрут', on_delete=models.CASCADE,
                                related_name='recruit_answers')
    question = models.ForeignKey(QuestionsList, 'Вопрос')
    answer = models.BooleanField('Ответ рекрута', null=True, blank=True)

    def __str__(self):
        return f'Рекрут {self.recruit.name}. Вопрос {self.question.title}. Ответ {self.answer}'
