from django.urls import path,include
from boke_apps import views

urlpatterns = [
    path('', views.home_main),
    path('add_data/', views.add_data),
    path('delete_data/', views.delete_data),
    path('update_data/', views.update_data),
    path('select_data/', views.select_data),
    path('test/',views.test),
    path('login/',views.login),
    path('register/',views.register)

]