from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    
    path('', views.home,  name="home"),
    #path('room/<str:pk>/', views.room, name="room"),
    #this will be line if in <h5>{{room.id}}--<a href="/room/{{room.id}}">{{room.name}}</a></h5> in home page
    path('room_page/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>', views.userProfile, name="user-profile"),


    path('test/', views.test, name="Test"),


# page name "create_room/" defination in folder views.
#  name of the page "create-room" now go to "home.html"
    path('create-topic/', views.createTopic, name="create-topic"),# From urls
    path('create-room/', views.createRoom, name="create-room"),# From urls
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),    
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),    
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),    

    # Other URL patterns
    path('export_rooms_csv/', views.export_rooms_csv, name='export-rooms-csv'),
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)),
]
