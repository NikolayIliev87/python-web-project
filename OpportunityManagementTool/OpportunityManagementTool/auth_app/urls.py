from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from OpportunityManagementTool.auth_app.views import UserLoginView, UserCreateView, \
    ChangeUserPasswordView, EditProfileView, UserDetailsView, log_out_user

urlpatterns = (
    path('login/', UserLoginView.as_view(), name='login user'),
    path('register/', UserCreateView.as_view(), name='request user'),
    path('logout/', log_out_user, name='logout user'),
    path('profile/<int:pk>/', UserDetailsView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', EditProfileView.as_view(), name='edit profile'),
    path('edit-password/', ChangeUserPasswordView.as_view(), name='change password'),
    path('edit-password-done/', RedirectView.as_view(url=reverse_lazy('index')), name='edit-password-done'),
)