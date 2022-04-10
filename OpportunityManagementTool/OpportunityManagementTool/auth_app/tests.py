from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse

from OpportunityManagementTool.auth_app.models import Profile

UserModel = get_user_model()


class ProfileDetailsViewTest(django_test.TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'test@abv.kk',
        'password': '12345qwer',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': 'User',
        'phone': '+111111',
        'is_manager': True,
    }

    def __create_valid_user_and_profile(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        return [user, profile]

    def test_when_opening_not_existing_profile__expect_404(self):
        response = self.client.get(reverse('profile', kwargs={
            'pk': 1,
        }))

        self.assertEqual(404, response.status_code)

    def test_when_all_valid__expect_correct_template(self):
        user, profile = self.__create_valid_user_and_profile()

        self.client.get(reverse('profile', kwargs={
            'pk': profile.pk
        }))


        self.assertTemplateUsed('auth_app/profile.html')

    def test_num_of_opps(self):
        pass
