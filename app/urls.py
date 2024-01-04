from django.urls import path,re_path
from .import views

app_name='students'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('create/',views.student_create,name='student_create'),
    path('list/',views.student_list,name='student_list'),
    path('deleted_students/', views.deleted_students, name='deleted_students'),
    re_path(r'^(?P<pk>\d+)/$', views.student_detail, name='student_detail'),
    re_path(r'^(?P<pk>\d+)/update/$',views.student_update,name='student_update'),
    re_path(r'^(?P<pk>\d+)/delete/$',views.student_delete, name='student_delete'),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
    path('student_attendance/', views.student_attendance, name='student_attendance'),
    path('view_attendance/',views.view_attendance,name='view_attendance'),

]