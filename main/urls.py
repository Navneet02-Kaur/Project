from django.urls import path
from . import views
from .views import logout_view

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.login_page, name='login'),
    path('toknowmore/', views.toknowmore, name='toknowmore'),
    path('offset/', views.offset, name='offset'),
    path('tips/', views.tips, name='tips'),
    path('calculator/', views.calculator, name='calculator'),
    path('signup/', views.signup, name='signup'),
    path('list_project/', views.list_project, name='list_project'),
    path('contribute/', views.contribute, name='contribution'),  # Fix name
    path('marketplace/', views.marketplace, name='marketplace'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', logout_view, name='logout'),  # Ensure this line is present
]
