from django import forms
from .models import *

# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ['content', 'photos']

#     def __init__(self, *args, **kwargs):
#         self.author = kwargs.pop('author', None)  # Получаем автора из аргументов
#         super().__init__(*args, **kwargs)

#     def save(self, commit=True):
#         post = super().save(commit=False)
#         post.author = self.author  # Устанавливаем автора перед сохранением
#         if commit:
#             post.save()
#             photos = self.cleaned_data.get('photos')
#             if photos:
#                 for photo in photos:
#                     photo_obj = Photo(image=photo, author=self.author)  # Устанавливаем автора для каждой фотографии
#                     photo_obj.save()
#                 post.photos.set(Photo.objects.filter(author=self.author, image__in=photos))
#         return post
#     def clean_photos(self):
#         photos = self.cleaned_data['photos']
#         if photos.count() > 10:
#             raise forms.ValidationError('Максимальное количество фотографий - 10.')
#         return photos

# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ['content', 'photos']

#     s

