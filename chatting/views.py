from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import EmptyPage, PageNotAnInteger,  Paginator, EmptyPage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from .models import Chat
from .serializers import MessageSerializer
from django.db.models import Count, Case, When, Q


@require_GET
@login_required(login_url='login')
def chat_add_friend(request, chat_id, user_id):
    chat = get_object_or_404(Chat, id = chat_id)
    user = get_object_or_404(User, id = user_id)
    if request.user not in chat.participants.all():
        return JsonResponse({"success": False, "message": "Вы не являетесь участником чата."}, status=403)
    if user not in chat.participants.all():
        chat.participants.add(user)
        return JsonResponse({"success": True, 'status': 'add', "message": "Пользователь добавлен."})
    else:
        chat.participants.remove(user)
        return JsonResponse({"success": True, 'status':'delete', "message": "Пользователь удалён."})




@login_required(login_url='error_404')
def get_chat_messages(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if not chat.participants.filter(id=request.user.id).exists():
        return JsonResponse({'error': 'Access Denied'}, status=403)

    messages = chat.messages.select_related('sender').all()
    paginator = Paginator(messages, 20)
    page_number = request.GET.get('page')
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        return JsonResponse({'error': 'Invalid page number'}, status=400)
    except EmptyPage:
        return JsonResponse({'error': 'Page not found'}, status=404)

    serialized_messages = MessageSerializer(page.object_list, many=True)
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse({'messages': serialized_messages.data, 'has_previous': page.has_previous(), 'has_next': page.has_next()})
    return JsonResponse({'error': 'Access Denied'}, status=403)




@login_required
def chat_details(request, chat_id):
    chat = Chat.objects.select_related('creator').get(id=chat_id)

    if not chat.participants.filter(id=request.user.id).exists():
        return redirect('chat_list')

    participants = chat.participants.select_related('profile').only('id', 'username', 'profile', 'profile__photo')
    chats = Chat.objects.filter(participants=request.user).prefetch_related('participants')
    context = {
        'chat': chat,
        'chat_id': chat_id,
        'participants': participants,
        'chats': chats,
    }

    return render(request, 'chat.html', context)




@login_required
def create_chat(request, user_id):
    # Получаем текущего пользователя и указанного пользователя
    current_user = request.user
    other_user = get_object_or_404(User, id=user_id)

    existing_chat = Chat.objects.filter(participants=current_user).filter(participants=other_user).last()
    if existing_chat and existing_chat.participants.count() == 2:
        return redirect('chat_details', chat_id=existing_chat.id)
    else:
        new_chat = Chat.objects.create(creator=request.user)
        new_chat.participants.add(current_user, other_user)

        # Перенаправляем на страницу нового чата
        return redirect('chat_details', chat_id=new_chat.id)




def mainpage(request):
    return render(request, 'mainpage.html')




from django.db.models import Count, Case, When, F, Max

@login_required
def chat_list(request):
    user = request.user

    chats = Chat.objects.filter(participants=user).prefetch_related('participants')
    
    context = {
        'chats': chats
    }
    return render(request, 'chat_list.html', context)

