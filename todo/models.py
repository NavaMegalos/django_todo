from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator


class Status(models.Model):
    description = models.CharField(max_length=15)


class Task(models.Model):
    description = models.CharField(max_length=255)
    status = models.ForeignKey("Status", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.description} ({self.status.description})"


class TodoList(models.Model):
    name = models.CharField(max_length=255)
    task = models.ManyToManyField("Task", through="TodoListTask")

    def __str__(self):
        return f"{self.name}"


class User(models.Model):
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    todo_list = models.ManyToManyField(TodoList, through="UserTodoList")

    def clean(self):
        if len(str(self.password)) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

    def __str__(self):
        return str(self.name)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password

        return check_password(raw_password, self.password)


class TodoListTask(models.Model):
    task = models.ForeignKey("Task", on_delete=models.CASCADE)
    todo_list = models.ForeignKey("TodoList", on_delete=models.CASCADE)
    assigned_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.description} - {self.todo_list.name}"

    class Meta:
        db_table = "todo_list_tasks"


class UserTodoList(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    todo_list = models.ForeignKey("TodoList", on_delete=models.CASCADE)
    assigned_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.todo_list.name}"

    class Meta:
        db_table = "user_todolist"
