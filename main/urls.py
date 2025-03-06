from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.login_page, name='login'),
    path('toknowmore/', views.toknowmore, name='toknowmore'),
    path('offset/', views.offset, name='offset'),
    path('tips/', views.tips, name='tips'),
    path('calculator/', views.calculator, name='calculator'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('list_project/', views.list_project, name='list_project'),
    path('contribution/', views.contribution, name='contribution'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('my_projects/', views.my_projects, name='my_projects'),
]
