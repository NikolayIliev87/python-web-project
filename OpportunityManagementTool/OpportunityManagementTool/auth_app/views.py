from django.contrib.auth import views as auth_views
from django.views import generic as views
from django.shortcuts import render
from django.urls import reverse_lazy

from OpportunityManagementTool.auth_app.forms import CreateProfileForm
from OpportunityManagementTool.auth_app.models import Profile


class UserCreateView(views.CreateView):
    form_class = CreateProfileForm
    template_name = 'auth_app/profile_create.html'
    success_url = reverse_lazy('index')


class ChangeUserPasswordView(auth_views.PasswordChangeView):
    template_name = 'auth_app/change_password.html'


class UserLoginView(auth_views.LoginView):
    template_name = 'auth_app/login_page.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class UserDetailsView(views.DetailView):
    model = Profile
    template_name = 'auth_app/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, *args, **kwargs):
        context= super().get_context_data(**kwargs)

        opps_total = 2

        context.update({
            'opps_total': opps_total,
        })

        return context


class EditProfileView(views.UpdateView):
    model = Profile
    template_name = 'auth_app/edit_profile.html'
    fields = ('first_name', 'last_name', 'phone', 'photo_url', 'is_manager', 'manager', 'group',)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})
