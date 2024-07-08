from django.urls import path
from . import views

urlpatterns = [
    path('', views.mailing_list, name='mailing_list'),
    path('<int:pk>/', views.mailing_detail, name='mailing_detail'),
    path('create/', views.mailing_create, name='mailing_create'),
    path('<int:pk>/update/', views.mailing_update, name='mailing_update'),
    path('<int:pk>/delete/', views.mailing_delete, name='mailing_delete'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
]
