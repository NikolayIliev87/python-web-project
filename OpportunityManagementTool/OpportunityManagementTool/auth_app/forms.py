from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model

from OpportunityManagementTool.auth_app.models import Profile, Manager


class CreateProfileForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LENGTH
    )
    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGTH
    )
    phone = forms.CharField(
        max_length=Profile.PHONE_MAX_LENGTH
    )
    photo_url = forms.URLField()

    is_manager = forms.BooleanField()

    manager = forms.EmailField(required=False)
    # manager = forms.ModelChoiceField(queryset=Manager.objects.values_list('email', flat=True), required=False)
    # group = forms.ModelChoiceField(queryset=BusinessGroup.objects.all(), to_field_name='name', required=False)
    group = forms.CharField(
        max_length=Profile.GROUP_NAME_MAX_LENGTH
    )

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            phone=self.cleaned_data['phone'],
            photo_url=self.cleaned_data['photo_url'],
            is_manager=self.cleaned_data['is_manager'],
            manager=self.cleaned_data['manager'],
            group=self.cleaned_data['group'],
            user=user,
        )

        manager = Manager(
            email=self.cleaned_data['email'],
            user=user,
        )

        if commit:
            profile.save()
            if self.cleaned_data['is_manager']:
                manager.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'phone', 'photo_url', 'is_manager', 'manager', 'group')



# class DeleteProfileForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for _, field in self.fields.items():
#             field.widget.attrs['disabled'] = True
#             field.required = False
#
#     def save(self, commit=True):
#         pets = list(self.instance.pet_set.all())
#         PetPhoto.objects.filter(tagget_pets__in=pets).delete()
#         self.instance.delete()
#         return self.instance
#
#     class Meta:
#         model = Profile
#         fields = ()
