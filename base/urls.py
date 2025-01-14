
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registeruser, name="register"),
    path('profile/<str:pk>/', views.userprofile, name="user-profile"),
    path('update-user/', views.updateuser, name="update-user"),
    path('topics/', views.topicsPage, name="topics"),
    path('room/<str:pk>/', views.room, name="room"),
    path('create-room/', views.creatroom, name="creat-room"),
    path('update-room/<str:pk>', views.updateroom, name="update-room"),
    path('delete-room/<str:pk>', views.deleteroom, name="delete-room"),
    path('delete-message/<str:pk>', views.deletemessage, name="delete-message"),
    path('activity/', views.activityPage, name="activity"),
    
]