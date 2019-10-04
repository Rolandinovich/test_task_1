import main.views as main
from django.urls import path

app_name = 'main'

urlpatterns = [
    path('', main.start_page, name='index'),
    path('recruit/create/', main.recruit_create, name='recruit_create'),
    path('recruit/finish_test/', main.finish_test, name='finish_test'),
    path('recruit/test/<int:pk>/', main.RecruitTest.as_view(), name='recruit_test'),
    path('sith/list/', main.sith_list, name='sith_list'),
    path('sith/detail/<int:pk>/', main.sith_detail, name='sith_detail'),
    path('sith/recruit_test_result/<int:pk>/', main.recruit_test_result, name='recruit_test_result'),
    path('sith/add_recruit/<int:pk_sith>/<int:pk_recruit>/', main.add_recruit, name='add_recruit'),
    path('sith/del_recruit/<int:pk_sith>/<int:pk_recruit>/', main.del_recruit, name='del_recruit'),
]
