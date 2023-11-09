from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Count, Exists, OuterRef, Subquery
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from .serializers import PostSerializer, CommentSerializer


@require_POST
@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        files = request.FILES.getlist('photos')
        if len(files) > 10:
            return JsonResponse({'success': False, 'message': 'Вы загрузили слишком много файлов. Максимальное количество приложений - 10.'})
        post = Post.objects.create(content=content, author=request.user)
        for file in files:
            photo = Photo.objects.create(image=file, author=request.user)
            post.photos.add(photo)
        serialized_post = PostSerializer(post)
        return JsonResponse({'success': True, 'message': 'Post created successfully', 'obj': serialized_post.data})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})




def feed(request):
    posts = Post.objects.select_related('author').prefetch_related('photos').annotate(
        like_count=Count('like', distinct=True),
        comment_count=Count('comment', distinct=True)
    ).order_by('-created_at')

    if request.user.is_authenticated:
        posts = posts.annotate(
            is_liked_by_user=Exists(Like.objects.filter(author=request.user, content_type=13, object_id=OuterRef("id"))),
        ).all()
    return render(request, 'post_list.html', {'posts': posts})




def post_detail(request, post_id):
    post = Post.objects.filter(id=post_id).select_related(
        'author__profile'
    ).prefetch_related(
        'photos'
    ).annotate(
        like_count=Count('like', distinct=True),
        comment_count=Count('comment', distinct=True),
    )

    comments = Comment.objects.filter(
        content_type=ContentType.objects.get_for_model(Post),
        object_id=post_id
    ).select_related(
        'user__profile'
    ).annotate(
        like_count=Count('like', distinct=True),
    ).order_by('-like_count')

    if request.user.is_authenticated:
        comments = comments.annotate(is_liked_by_user=Exists(
            Like.objects.filter(
                author=request.user,
                content_type=ContentType.objects.get_for_model(Comment),
                object_id=OuterRef('id')
            )
        ))
        post = post.annotate(is_liked_by_user=Exists(
            Like.objects.filter(
                author=request.user, 
                content_type=ContentType.objects.get_for_model(Post), 
                object_id=post_id
            )
        ))

    return render(request, 'post_detail.html', {
        'post': post.first(),
        'comments': comments
    })


@require_GET
def like_object(request, content_type_id, object_id):
    content_type = get_object_or_404(ContentType, id=content_type_id)
    model_name = content_type.model_class()._meta.model_name
    if not request.user.is_authenticated:
        login_url = reverse('login')
        try:
            current_url = reverse(model_name, args=[object_id,])
        except:
            current_url = reverse('feed')
        redirect_url = f"{login_url}?next={current_url}"
        message = f'<a href="{redirect_url}">Авторизуйтесь чтобы оценить эту запись.</a>'
        return JsonResponse({"success": False, "message": message})
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        obj = get_object_or_404(content_type.model_class(), id=object_id)
        # Проверяем, был ли уже поставлен лайк для данного пользователя и объекта
        if not Like.objects.filter(content_type=content_type, object_id=obj.id, author=request.user).exists():
            # Создаем новый лайк для пользователя и объекта
            like = Like(content_type=content_type, object_id=obj.id, author=request.user)
            like.save()
            likes = Like.objects.filter(content_type=content_type, object_id=obj.id).count()
            return JsonResponse({"success":True, "liked": True, "likes": likes})
        else: 
            Like.objects.filter(content_type=content_type, object_id=obj.id, author=request.user).delete()
            likes = Like.objects.filter(content_type=content_type, object_id=obj.id).count()
            return JsonResponse({"success": True, "liked": False, "likes": likes})
    return JsonResponse({"success": False, "message": "Возникла ошибка."})

@login_required
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get('content')
    user = request.user
    
    comment = Comment.objects.create(
        content_type=post.content_type,
        object_id=post.id,
        content_object=post,
        user=user,
        content=content
    )
    serialized_comment = CommentSerializer(comment)
    return JsonResponse({'success': True, 'message': 'Comment created successfully', 'obj': serialized_comment.data})