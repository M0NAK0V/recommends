from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name= "login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('course/<str:pk>', views.course, name='course'),
    path('courses', views.courses, name='courses'),
    

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    # path('achievements/', AchievementList.as_view(), name='achievements-list'),
    # path('achievements/create/', AchievementCreate.as_view(), name='achievements-create'),
    # path('achievements/add/', AchievementAdd.as_view(), name='achievements-add'),

    path('courses/create',views.create_course, name='courses-create'),
    path('courses/<int:pk>/add_question/', views.add_question, name='add_question'),
    path('courses/<int:pk>/questions/', views.course_questions, name='course_questions'),
]