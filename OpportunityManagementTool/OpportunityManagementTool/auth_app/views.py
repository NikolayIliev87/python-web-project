from django.contrib.auth import views as auth_views
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Q

from OpportunityManagementTool.auth_app.forms import CreateProfileForm
from OpportunityManagementTool.auth_app.models import Profile
from OpportunityManagementTool.web.models import Opportunity


class UserCreateView(views.CreateView):
    form_class = CreateProfileForm
    template_name = 'auth_app/profile_create.html'
    success_url = reverse_lazy('index')


class ChangeUserPasswordView(auth_views.PasswordChangeView):
    template_name = 'auth_app/change_password.html'
    success_url = reverse_lazy('edit-password-done')


class UserLoginView(auth_views.LoginView):
    template_name = 'auth_app/login_page.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class UserDetailsView(auth_mixin.LoginRequiredMixin, views.DetailView):
    model = Profile
    template_name = 'auth_app/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, *args, **kwargs):
        context= super().get_context_data(**kwargs)

        opps_total = len(list(Opportunity.objects.filter(Q(owner=self.request.user) & Q(to_be_deleted=False))))

        context.update({
            'opps_total': opps_total,
        })

        return context

    def get_queryset(self):
        return Profile.objects.filter(pk=self.request.user.pk)



class EditProfileView(auth_mixin.LoginRequiredMixin, views.UpdateView):
    model = Profile
    template_name = 'auth_app/edit_profile.html'
    fields = ('first_name', 'last_name', 'phone', 'photo_url', 'is_manager', 'manager', 'group',)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        return Profile.objects.filter(pk=self.request.user.pk)
