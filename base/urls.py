
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('login/register/', views.registeruser, name="register"),
    path('room/<str:pk>/', views.room, name="room"),
    path('create-room/', views.creatroom, name="creat-room"),
    path('update-room/<str:pk>', views.updateroom, name="update-room"),
    path('delete-room/<str:pk>', views.deleteroom, name="delete-room"),
    path('delete-message/<str:pk>', views.deletemessage, name="delete-message"),
    
]