from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.mail import send_mail
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('catalog:home')  # Перенаправление после успешного редактирования
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'users/edit_profile.html', {'form': form})


# Регистрация пользователя
class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        try:
            send_mail(
                'Добро пожаловать!',
                'Спасибо за регистрацию на нашем сайте.',
                'anastasianikolaeva666@yandex.ru',
                [user.email],
                fail_silently=False,
            )
            messages.success(self.request, 'Письмо с подтверждением отправлено!')
        except Exception as e:
            messages.error(self.request, f'Ошибка при отправке письма: {str(e)}')

        return super().form_valid(form)


# Вход пользователя
class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        messages.success(self.request, 'Вы успешно вошли в систему!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Неверный логин или пароль.')
        return super().form_invalid(form)


# Выход пользователя
class LogoutConfirmView(TemplateView):
    template_name = 'users/logout_confirm.html'


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('catalog:home')

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Вы успешно вышли из системы!')
        return super().post(request, *args, **kwargs)


class DeleteUserView(LoginRequiredMixin, View):
    def get(self, request):
        # Отображение страницы подтверждения удаления
        return render(request, 'users/delete_user.html')

    def post(self, request):
        # Удаление пользователя
        user = request.user
        user.delete()
        messages.success(request, 'Ваш аккаунт был успешно удален.')
        return redirect('catalog:home')
