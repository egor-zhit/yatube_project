from core.models import CreatedModel
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(Group,
                              on_delete=models.SET_NULL,
                              related_name='posts',
                              blank=True, null=True)
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(CreatedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="comments")
    text = models.TextField()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="follower")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="following")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"], name="unique_follow"
            )
        ]
