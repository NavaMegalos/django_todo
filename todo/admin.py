from django.contrib import admin
from .models import User, TodoList, Task, Status, UserTodoList

admin.site.register(User)
admin.site.register(TodoList)
admin.site.register(Task)
admin.site.register(Status)
admin.site.register(UserTodoList)
