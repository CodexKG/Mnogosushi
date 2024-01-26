from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView

from apps.settings.models import Setting
from apps.users.models import User
from apps.products.models import ReviewProduct , Product
# Create your views here.
def register(request):
    setting = Setting.objects.latest('id')
    if request.method == "POST":
        print('register')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            if username and email and password and confirm_password:
                try:
                    user = User.objects.create(username = username, email = email)
                    user.set_password(password)
                    user.save()
                    user = User.objects.get(username = username)
                    user = authenticate(username = username, password = password)
                    login(request, user)
                    return redirect('index')
                except:
                    return redirect('register_error')
            else:
                return redirect('register_error')
        else:
            return redirect('register_error')
    context = {
        'setting' : setting,
    }
    return render(request, 'users/register.html', context)

def user_login(request):
    setting = Setting.objects.latest('id')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = username)
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('index')
        except:
            return redirect('user_not_found')
    context = {
        'setting' : setting,
    }
    return render(request, 'users/login.html', context)

def profile(request, username):
    user = User.objects.get(username = username)
    product = Product.objects.all()
    reviews = ReviewProduct.objects.all()
    # reviews = ReviewProduct.objects.filter(product_id=id).order_by('-created')[:5]
    if request.method == "POST":
        if 'update' in request.POST:
            print("UPDATE")
            profile_image = request.FILES.get('profile_image')
            print(profile_image)
            user_username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            user.username = user_username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email 
            user.phone = phone
            if profile_image:
                user.profile_image = profile_image
            user.save()
            return redirect('profile', user.username)

    return render(request, 'users/detail.html', locals())

def delete_review(request, review_id):
    review = get_object_or_404(ReviewProduct, id=review_id)

    # Проверка, что пользователь имеет право удалять отзыв (например, проверка прав доступа)
    if request.user == review.user:
        review.delete()
    return redirect('index')

class CustomLoginView(LoginView):
    template_name = 'admin/custom_login.html'

    def post(self, request, *args, **kwargs):
        # Обработка POST-запроса, когда пользователь отправляет форму входа
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Вход выполнен успешно, можно перенаправить пользователя на нужную страницу
            return redirect('admin:index')
        else:
            # Ошибка входа, выполните обработку ошибки
            return render(request, self.template_name, {'error_message': 'Ошибка входа'})