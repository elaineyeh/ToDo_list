from rest_framework import permissions, viewsets
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied

from app.todo.models import Todo
from app.todo.serializers import TodoSerializer, UserSerializer


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')

        if self.action == 'list':
            if user_id is not None:
                if int(user_id) == int(self.request.user.pk):
                    queryset = self.queryset.filter(user_id=user_id)
                    return queryset
                else:
                    raise PermissionDenied()
            return self.queryset

        return Todo.objects.filter(user_id=self.request.user.pk)

    def get_permissions(self):
        user_id = self.request.query_params.get('user_id')
        if self.action == 'list':
            if user_id is None:
                self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
