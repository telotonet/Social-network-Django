from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator
from .models import Profile, FriendRequest
from .forms import RegistrationForm, LoginForm
from .serializers import UserSerializer
from django.urls import reverse
from django.db.models import BooleanField, Case, When, Value, Exists, OuterRef, Q


User = get_user_model()




def friendlist(request):
    user = request.user
    friend_requests = FriendRequest.objects.filter(
        Q(from_user=user) | Q(to_user=user), is_accepted=True
    )
    friends = User.objects.select_related('profile').filter(
        Q(id__in=friend_requests.values('from_user_id')) | Q(id__in=friend_requests.values('to_user_id'))
    ).exclude(id=user.pk).distinct()

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse(UserSerializer(friends, many=True).data, safe=False)

    paginator = Paginator(friends, 10)
    page_number = request.GET.get('page')
    friends = paginator.get_page(page_number)
    return render(request, 'friendlist.html', {'friends': friends})



    
@require_GET
def send_friend_request(request, user_id):
    if not request.user.is_authenticated:
        login_url = reverse('login')
        current_url = request.path
        redirect_url = f"{login_url}?next={current_url}"
        message = f'<a href="{redirect_url}">Авторизуйтесь чтобы добавлять в друзья.</a>'
        return JsonResponse({"success": False, "message": message})
    if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
        try:
            from_user = request.user
            to_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"success": False, "message": "Неверный идентификатор пользователя."})
        
        if from_user == to_user:
            return JsonResponse({"success": False, "message": "Вы не можете отправить себе запрос в друзья."})
        
        friend_qs = FriendRequest.objects.filter(Q(from_user=to_user, to_user=from_user) | Q(from_user=from_user, to_user=to_user))

        if friend_qs.filter(is_accepted = False).exists() and friend_qs.first().from_user==request.user:
            friend_qs.first().delete()
            return JsonResponse({"success": True, "status": 'decline', "message": "Запрос в друзья отменен."})
        if friend_qs.filter(is_accepted = False).exists() and friend_qs.first().to_user==request.user:
            friend_qs.update(is_accepted = True)
            return JsonResponse({"success": True, "status": 'accept', "message": "Запрос в друзья принят."})
        if friend_qs.filter(is_accepted = True).exists():
            friend_qs.first().delete()
            return JsonResponse({"success": True, "status": 'delete', "message": "Друг удалён."})
        friend_request, created = FriendRequest.objects.update_or_create(
            from_user=from_user,
            to_user=to_user,
            defaults={"is_accepted": False}
        )
        if created:
            return JsonResponse({"success": True, "status": 'sent', "message": "Запрос в друзья отправлен."})
        # if friend_qs.filter(is_accepted=True).exists():
        #     friend_qs.delete()
        #     return JsonResponse({"success": True, "sent": False, "message": "Запрос в друзья отменен."})

        # friend_request, created = FriendRequest.objects.update_or_create(
        #     from_user=from_user,
        #     to_user=to_user,
        #     defaults={"is_accepted": False}
        # )
        # if friend_qs.filter(is_accepted=False).exists():
        #     friend_request.is_accepted=True
        #     friend_request.save()
        #     return JsonResponse({"success": True, "friends": True, "message": "Запрос в друзья принят."})

        # if created:
        #     return JsonResponse({"success": True, "sent": True, "message": "Запрос в друзья отправлен."})
        # else:
        #     friend_request.delete()
        #     return JsonResponse({"success": True, "sent": False, "message": "Запрос в друзья отменен."})

    return JsonResponse({"success": False, "message": "Invalid request."})



@require_GET
def get_user_ajax(request, user_id):
    if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return HttpResponseForbidden("Forbidden")
    if not user_id:
        return JsonResponse({'error': 'User ID is required'}, status=400)
    try:
        friend_requests = FriendRequest.objects
        user = User.objects.select_related('profile').annotate(
            is_friend_request_sent=Exists(friend_requests.filter(from_user=request.user.id, to_user_id=OuterRef('id'), is_accepted=False)),
            is_friend_request_received=Exists(friend_requests.filter(from_user=OuterRef('id'), to_user_id=request.user.pk, is_accepted=False)),
            is_friend=Exists(friend_requests.filter(to_user_id=OuterRef('id'), is_accepted=True))
        ).get(id=user_id)

    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    serializer = UserSerializer(user)
    return JsonResponse(serializer.data)




@login_required(login_url='login')
def profiles(request):
    user = request.user
    friend_requests = FriendRequest.objects.filter(Q(from_user=user) | Q(to_user=user))
    users_with_profiles = User.objects.select_related('profile').exclude(pk=user.pk).annotate(
        is_friend_request_sent=Case(
            When(id__in=friend_requests.values_list('to_user', flat=True), then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        ),
        is_friend_request_received=Case(
            When(id__in=friend_requests.values_list('from_user', flat=True), then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        ),
        is_friend=Case(
            When(id__in=friend_requests.filter(is_accepted=True).values_list('from_user', flat=True), then=Value(True)),
            When(id__in=friend_requests.filter(is_accepted=True).values_list('to_user', flat=True), then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        ),
    )
    
    paginator = Paginator(users_with_profiles, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'profiles.html', {'page_obj': page_obj})






def signup(request):
    if request.user.is_authenticated:
        return redirect('mainpage')
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('mainpage')
        else:
             for errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form':form})




def user_login(request):
    if request.user.is_authenticated:
        return redirect('mainpage')
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print('hello')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next', 'mainpage'))
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})




@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('mainpage')
