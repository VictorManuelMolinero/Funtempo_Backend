from django.contrib import admin
from django.urls import path

from Controllers import userController, scheduleController

urlpatterns = [
    # URLs for UserController
    path('users/', userController.UserController.getAll),
    path('users/post/', userController.UserController.as_view()),
    path('users/<str:username>/', userController.UserController.as_view()),

    # URLs for ScheduleController
    path('schedules/', scheduleController.ScheduleController.getAll),
    path('schedules/add/', scheduleController.ScheduleController.as_view()),
    path('schedules/delete/', scheduleController.ScheduleController.as_view()),
    path('schedules/edit/<int:schedule_id>/', scheduleController.ScheduleController.as_view()),
    path('schedules/<str:username>/', scheduleController.ScheduleController.as_view()),   
]
