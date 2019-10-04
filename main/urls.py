import main.views as main
from django.urls import path

app_name = 'main'

urlpatterns = [
    path('', main.start_page, name='index'),
    path('recruit/create/', main.recruit_create, name='recruit_create'),
    path('recruit/finish_test/', main.finish_test, name='finish_test'),
    path('recruit/test/<int:pk>/', main.RecruitTest.as_view(), name='recruit_test'),
    path('sith/list/', main.sith_list, name='sith_list'),
]
