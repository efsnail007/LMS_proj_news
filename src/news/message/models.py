from django.db import models
from django.conf import settings


class Dialog(models.Model):
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def get_absolute_url(self):
        return 'message:chats', (), {'chat_id': self.pk }

class Message(models.Model):
    sender =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_1')
    reciever = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_2')
    message = models.TextField('Сообщение')
    created_at = models.DateTimeField('Дата отправки сообщения', auto_now_add=True)
    is_readed = models.BooleanField('Прочитано', default=False)

    def __str__(self):
        return f'{self.sender}, {self.reciever}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    


