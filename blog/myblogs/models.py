from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.


class Tag(models.Model):
    name = models.CharField("タグ名", max_length=255, unique=True)

    def __str__(self):
        if hasattr(self, 'post_count'):
            return f'{self.name}({self.post_count})'
        else:
            return self.name


class Post(models.Model):
    title = models.CharField(("タイトル"), max_length=32)
    text = models.TextField("本文")
    tags = models.ManyToManyField(Tag, verbose_name=("タグ"), blank=True)

    relation_post = models.ManyToManyField(
        "self", verbose_name=("関連記事"), blank=True)
    is_public = models.BooleanField(("公開可能か？"), default=True)
    description = models.TextField(("記事の説明"), max_length=130)
    keywords = models.CharField(
        ("記事のキーワード"), max_length=255, default="記事のキーワード")
    created_at = models.DateTimeField(("作成日"), default=timezone.now)
    updated_at = models.DateTimeField(("更新日"), default=timezone.now)

    def __str__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(("名前"), max_length=255, default='名無し')
    text = models.TextField(("本文"))
    target = models.ForeignKey(
        Post, on_delete=models.CASCADE, verbose_name="対象記事")
    created_at = models.DateTimeField(("作成日"), default=timezone.now)
    email = models.EmailField(
        'メールアドレス', blank=True, help_text='入力しておくと、返信があった際に通知します。コメント欄には表示されません。')

    def __str__(self):
        return self.text[:20]


class Reply(models.Model):
    name = models.CharField(("名前"), max_length=255, default='名無し')
    text = models.TextField(("本文"))
    target = models.ForeignKey(
        Comment, on_delete=models.CASCADE, verbose_name=("対象コメント"))
    created_at = models.DateTimeField(("作成日"), default=timezone.now)

    def __str__(self):
        return self.text[:20]
