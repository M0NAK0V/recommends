from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name= "login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('bigcourse/<str:pk>/course/<str:pk_1>/', views.course, name='course'),
    path('bigcourse/<str:pk>/results/', views.results, name='results'),
    path('courses/', views.courses, name='courses'),
    path('bigcourse/<str:pk>', views.bigcourse, name='bigcourse'),
    path('bigcourses/', views.bigcourses, name='bigcourses'),

    

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    # path('achievements/', AchievementList.as_view(), name='achievements-list'),
    # path('achievements/create/', AchievementCreate.as_view(), name='achievements-create'),
    # path('achievements/add/', AchievementAdd.as_view(), name='achievements-add')

    path('bigcourse/<str:pk>/courses/create',views.create_course, name='courses-create'),
    path('bigcourse/<str:pk>/course/<str:pk_1>/add_question/', views.add_question, name='add_question'),
    path('bigcourse/<str:pk>/course/<int:pk_1>/questions/', views.course_questions, name='course_questions'),
    path('bigcourse/<str:pk>/course/<int:pk_1>/solve/', views.course_solve, name='course_solve'),
    path('bigcourses/create',views.create_bigcourse, name='bigcourses-create'),
    


]