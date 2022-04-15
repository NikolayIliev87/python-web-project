from datetime import date
from django import test as django_test
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse

from OpportunityManagementTool.auth_app.models import Profile, Manager
from OpportunityManagementTool.web.models import Opportunity, Client, BusinessGroup, Product

UserModel = get_user_model()


class MainCatalogsAndTheirDetailsForUsersTest(django_test.TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'test@abv.kk',
        'password': '12345qwer',
        'is_staff': True
    }

    VALID_USER_CREDENTIALS2 = {
        'email': 'test@abv.kk',
        'password': '12345qwer',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': 'User',
        'phone': '+111111',
        'is_manager': True,
    }

    VALID_PROFILE_DATA2 = {
        'first_name': 'Test',
        'last_name': 'User',
        'phone': '+111111',
        'is_manager': False,
    }

    VALID_OPPORTUNITY_DATA = {
        'name': "TESTOPP",
        'description': 'SOME OPP',
        'close_date': date(2022, 4, 13),
        'status': 'WON',
    }

    VALID_CLIENT_DATA = {
        'name': "TESTCLIENT",
        'city': 'SOME OPP',
        'email': 'testclient@abv.kk',
        'phone': '+99999',
        'discount': '1',
    }

    VALID_BGROUP_DATA = {
        'name': "TESTBG",
    }

    VALID_PRODUCT_DATA = {
        'name': "TESTPRODUCT",
        'price': '10'
    }

    def __create_valid_user_and_profile(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        return [user, profile]

    def __create_valid_user_and_profileNonManager(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS2)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA2,
            user=user,
        )

        return [user, profile]

    def test_home_page_correct_template_not_logged_in(self):
        user, profile = self.__create_valid_user_and_profile()
        response = self.client.get(reverse('index'))

        self.assertTemplateUsed(response=response, template_name='web/home_page_profile.html')
        self.assertContains(response, 'Welcome To Opportunity Management Tool!')

    def test_home_page_correct_template_logged_in(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('index'))

        self.assertTemplateUsed(response=response, template_name='web/home_page_profile.html')
        self.assertContains(response, f'Welcome to your opportunity portal { profile.user }!')

    def test_clients_list_correct_template_when_logged_in(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        client = Client.objects.create(**self.VALID_CLIENT_DATA)
        response = self.client.get(reverse('clients catalog'))

        self.assertTemplateUsed(response=response, template_name='web/clients_list.html')
        self.assertContains(response, '</a>', 5)

    def test_client_details_correct_template_when_logged_in_manager(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        client = Client.objects.create(**self.VALID_CLIENT_DATA)
        response = self.client.get(reverse('details client', kwargs={
            'pk': client.pk,
        }))

        self.assertTemplateUsed(response=response, template_name='web/client_details.html')
        self.assertContains(response, 'Client Name')
        self.assertContains(response, 'editclient', 1)

    def test_client_details_correct_template_when_logged_in_non_manager(self):
        user, profile = self.__create_valid_user_and_profileNonManager()

        self.client.login(**self.VALID_USER_CREDENTIALS)

        client = Client.objects.create(**self.VALID_CLIENT_DATA)
        response = self.client.get(reverse('details client', kwargs={
            'pk': client.pk,
        }))

        self.assertTemplateUsed(response=response, template_name='web/client_details.html')
        self.assertContains(response, 'Client Name')
        self.assertContains(response, '</a>', 4)

    def test_clients_list_correct_template_not_logged_in(self):
        user, profile = self.__create_valid_user_and_profile()
        response = self.client.get(reverse('clients catalog'))

        self.assertTemplateNotUsed(response=response, template_name='web/clients_list.html')

    def test_business_group_correct_template_when_logged_in(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        bgroup = BusinessGroup.objects.create(**self.VALID_BGROUP_DATA)
        response = self.client.get(reverse('businessgroup catalog'))

        self.assertTemplateUsed(response=response, template_name='web/business_group_list.html')
        self.assertContains(response, 'All Business Groups')
        self.assertContains(response, '</a>', 4)

    def test_business_group_list_correct_template_not_logged_in(self):
        user, profile = self.__create_valid_user_and_profile()
        response = self.client.get(reverse('businessgroup catalog'))

        self.assertTemplateNotUsed(response=response, template_name='web/business_group_list.html')

    def test_products_list_correct_template_when_logged_in(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        bgroup = BusinessGroup.objects.create(**self.VALID_BGROUP_DATA)
        product = Product.objects.create(**self.VALID_PRODUCT_DATA, group=bgroup)
        response = self.client.get(reverse('products catalog'))

        self.assertTemplateUsed(response=response, template_name='web/products_list.html')
        self.assertContains(response, 'All Products')
        self.assertContains(response, '</a>', 4)

    def test_products_list_correct_template_not_logged_in(self):
        user, profile = self.__create_valid_user_and_profile()
        response = self.client.get(reverse('products catalog'))

        self.assertTemplateNotUsed(response=response, template_name='web/products_list.html')

    def test_managers_list_correct_template_when_logged_in(self):
        user, profile = self.__create_valid_user_and_profile()
        if profile.is_manager:
            manager = Manager.objects.create(email=user.email, user=user)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('managers catalog'))

        self.assertTemplateUsed(response=response, template_name='web/managers_list.html')
        self.assertContains(response, 'All Available Managers')
        self.assertContains(response, '</p>', 2)

    def test_managers_list_correct_template_not_logged_in(self):
        user, profile = self.__create_valid_user_and_profile()
        response = self.client.get(reverse('managers catalog'))

        self.assertTemplateNotUsed(response=response, template_name='web/managers_list.html')

class OpportunityViewsTest(django_test.TestCase):
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

    VALID_PROFILE_DATA2 = {
        'first_name': 'Test',
        'last_name': 'User',
        'phone': '+111111',
        'is_manager': False,
    }

    VALID_OPPORTUNITY_DATA = {
        'name': "TESTOPP",
        'description': 'SOME OPP',
        'close_date': date(2022, 4, 13),
        'status': 'WON',
    }

    VALID_CLIENT_DATA = {
        'name': "TESTCLIENT",
        'city': 'SOME OPP',
        'email': 'testclient@abv.kk',
        'phone': '+99999',
        'discount': '1',
    }

    VALID_BGROUP_DATA = {
        'name': "TESTBG",
    }

    VALID_PRODUCT_DATA = {
        'name': "TESTPRODUCT",
        'price': '10'
    }

    def __create_valid_user_and_profile(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        return [user, profile]

    def __create_valid_user_and_profileNonManager(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA2,
            user=user,
        )

        return [user, profile]

    def test_dashboard_correct_data_when_logged_in(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        opportunity = Opportunity.objects.create(
            **self.VALID_OPPORTUNITY_DATA,
            owner=user,
        )
        response = self.client.get(reverse('dashboard'))
        opps = len(Opportunity.objects.all())

        self.assertTemplateUsed(response=response, template_name='web/dashboard.html')
        self.assertContains(response, 'Yours/team activities:')
        self.assertContains(response, 'detailbtn', 1)
        self.assertContains(response, f'# Opps: {opps}')
        self.assertContains(response, f'Opp Name: {opportunity.name}')
        self.assertContains(response, f'Owner: {user.email}')
        self.assertContains(response, f'Status: {opportunity.status}')
        self.assertContains(response, f'Client: {opportunity.client}')
        self.assertContains(response, 'Total Net: 0.00$')
        self.assertNotContains(response, 'Opp Net Amount:')
        self.assertContains(response, 'Page 1')
        self.assertNotContains(response, 'Next')
        self.assertNotContains(response, 'Last')

    def test_dashboard_correct_data_when_not_logged_in(self):
        user, profile = self.__create_valid_user_and_profile()
        response = self.client.get(reverse('dashboard'))

        self.assertTemplateNotUsed(response=response, template_name='web/dashboard.html')
