from django.contrib import admin

# Register your models here.


from main.models import Planet, Recruit, Sith, TestTrial, QuestionsList, Answer

admin.site.register(Planet)
admin.site.register(Recruit)
admin.site.register(Sith)
admin.site.register(TestTrial)
admin.site.register(QuestionsList)
admin.site.register(Answer)
