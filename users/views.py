from typing import Any

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.db.models import Prefetch
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache

from .forms import UserLoginForm, UserRegistrationForm, ProfileForm, UserPasswordChangeForm
from .models import User

from carts.models import Cart
from orders.models import Order, OrderItem
from common.mixins import CacheMixin

from dotenv import load_dotenv
import os

load_dotenv()


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    # success_url = reverse_lazy('main:index')  # формируется только после инициализацией


    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        not_allowed_pages = [reverse('user:logout'), reverse('user:password_change'),]
        if redirect_page and redirect_page not in not_allowed_pages :
            return redirect_page
        return reverse_lazy('main:index')
        

    def form_valid(self, form):
        session_key = self.request.session.session_key

        user = form.get_user()

        if user:
            auth.login(self.request, user)
            messages.success(self.request, f"{user.username}, Вы вошли в аккаунт!")
            if session_key:
                # delete old authorized user carts
                forgot_carts = Cart.objects.filter(user=user)
                if forgot_carts.exists():
                    forgot_carts.delete()
                # add new authorized user carts from anonimous session
                Cart.objects.filter(session_key=session_key).update(user=user)
            
                return HttpResponseRedirect(self.get_success_url())


        return super().form_valid(form)
    

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Login"
        return context
    

class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

        messages.success(self.request, f"{self.request.user.username}, Вы успешно зарегистрировались и вошли в аккаунт!")
        return HttpResponseRedirect(self.success_url)
    

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Registration"
        return context
    


class UserProfileView(LoginRequiredMixin, CacheMixin, UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, "Профиль успешно обновлен!")
        return super().form_valid(form)
    

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Profile"
    

        orders = (
        Order.objects.filter(user=self.request.user)
        .prefetch_related(
            Prefetch(
                'orderitem_set',
                queryset=OrderItem.objects.select_related('product'),
                )
            )
            .order_by("-id")
        )

        context["orders"] = self.set_get_cache(orders, f"user_{self.request.user.id}_orders", 60 * 2)
        return context
    

class UsersCartView(TemplateView):
    template_name = 'users/users_cart.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Корзина"
        return context
    


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/password/password_change.html'
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        messages.success(self.request, 'Пароль успешно изменен!')
        return super().form_valid(form)

    

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Смена пароля"
        return context
    


class UserPasswordResetView(PasswordResetView):
    template_name = 'users/password/password_reset.html'
    email_template_name = 'users/password/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')


    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Восстановление пароля"
        return context
    
    

class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/password/password_reset_done.html"



class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password/password_reset_confirm.html'
    success_url = reverse_lazy('users:login')

    def get_success_url(self):
        messages.success(self.request, 'Пароль успешно изменен')
        return super().get_success_url()
    



@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse('main:index'))




# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)

#             session_key = request.session.session_key

#             if user:
#                 auth.login(request, user)
#                 messages.success(request, f"{username}, Вы вошли в аккаунт!")

#                 if session_key:
#                     # delete old authorized user carts
#                     forgot_carts = Cart.objects.filter(user=user)
#                     if forgot_carts.exists():
#                         forgot_carts.delete()
#                         # add new authorized user carts from anonimous session

#                     Cart.objects.filter(session_key=session_key).update(user=user)

#                 redirect_page = request.POST.get('next', None)
#                 if redirect_page and redirect_page != reverse('user:logout'):
#                     return HttpResponseRedirect(request.POST.get('next'))

#                 return HttpResponseRedirect(reverse('main:index'))
#     else:
#         form = UserLoginForm()


#     context = {
#         'title': 'Home - Login',
#         'form': form,
#     }

#     return render(request, 'users/login.html', context)


# def registration(request):
#     if request.method == "POST":
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():

#             session_key = request.session.session_key

#             form.save()
#             user = form.instance
#             auth.login(request, user)
#             messages.success(request, f"{request.user.username}, Вы успешно зарегистрировались и вошли в аккаунт!")

#             if session_key:
#                 Cart.objects.filter(session_key=session_key).update(user=user)

#             return HttpResponseRedirect(reverse("main:index"))
#     else:
#         form = UserRegistrationForm()


#     context = {
#         'title': 'Home - Registration',
#         'form': form

#     }

#     return render(request, 'users/registration.html', context)


# @login_required
# def profile(request):
#     if request.method == "POST":
#         form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Профиль успешно обновлен!")
#             return HttpResponseRedirect(reverse('user:profile'))
#     else:
#         form = ProfileForm(instance=request.user)

#     orders = (
#         Order.objects.filter(user=request.user)
#         .prefetch_related(
#             Prefetch(
#                 'orderitem_set',
#                 queryset=OrderItem.objects.select_related('product'),
#                 )
#             )
#             .order_by("-id")
#         )

#     context = {
#         'title': 'Home - Profile',
#         'form': form,
#         'orders': orders
#     }

#     return render(request, 'users/profile.html', context)


# def users_cart(request):
#     return render(request, 'users/users_cart.html')