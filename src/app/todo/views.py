from rest_framework import permissions, viewsets
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User

from app.todo.models import Todo
from app.todo.serializers import TodoSerializer, UserSerializer


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    def get_queryset(self):
        return Todo.objects.filter(user_id=self.request.user.pk)


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
