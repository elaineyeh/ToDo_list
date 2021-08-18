from rest_framework import routers
from django.urls import path, include
from app.todo.views import TodoViewSet

route = routers.DefaultRouter(trailing_slash=True)
route.register('todo', TodoViewSet)

urlpatterns = [
    path('', include(route.urls))
]
