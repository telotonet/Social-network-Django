from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

def validate_max_files(value):
    if len(value)>10:
        return ValidationError('Максимальное количество файлов - 10')

class Post(models.Model):
    content    = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author     = models.ForeignKey(User, on_delete=models.CASCADE)
    like       = GenericRelation("Like")
    comment    = GenericRelation("Comment")
    photos     = models.ManyToManyField('Photo', blank=True,)

    class Meta:
        ordering = ['-created_at', 'content']

    def __str__(self):
        return f"Post by {self.author.username}"
    
    def get_absolute_url(self):
        return reverse('post', args=[self.pk])
    
    def clean(self):
        super().clean()
        if self.photos.count() > 10:
            raise ValidationError('Максимальное количество фотографий - 10.')

class Photo(models.Model):
    image = models.ImageField(upload_to='post_photos/',)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    like = GenericRelation("Like")
    comment = GenericRelation("Comment")

    def __str__(self):
        return str(self.image)
    
class Comment(models.Model):
    content_type   = models.ForeignKey(ContentType, on_delete = models.CASCADE)
    object_id      = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    content        = models.TextField(max_length=3000)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)
    like           = GenericRelation("Like")
    def __str__(self):
        return f"Commented by {self.user.username} on {self.content_type}"

class Like(models.Model):
    content_type   = models.ForeignKey(ContentType, on_delete = models.CASCADE)
    object_id      = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    author         = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"Liked by {self.author.username} on {self.content_type}"
