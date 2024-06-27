from django.db import models
from django.conf import settings



class Tags(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField('Заголовок новости', max_length=100, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор', on_delete=models.CASCADE)
    text = models.TextField('Текст новости')
    tags = models.ManyToManyField(Tags)
    created_at = models.DateTimeField('Дата публикации', auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def total_likes(self):
        return self.like.count()

class Addition(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    file = models.FileField(upload_to='news/%Y/%m/%d/')

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, verbose_name='Новость', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField('Текст комментария', max_length=2000)
    # replied_on = models.ForeignKey('Comment', on_delete=models.SET_NULL, null=True, blank=True, related_name="replies")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}, {self.item}'

    class Meta:
        verbose_name = 'Комменатрий'
        verbose_name_plural = 'Комментарии'

class Feedback(models.Model):
    text_feedback = models.TextField(default='Жалоба')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='feedback')

    def __str__(self):
        return f'{self.user}, {self.item}'

    class Meta:
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'