from django import forms
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy

from OpportunityManagementTool.web.models import Opportunity, Client, Product, BusinessGroup, OpportunityProducts


#OK
class CreateOpportunityForm(forms.ModelForm):
    # as owner is hidden from the form to be populated should be updated init and save with owner
    def __init__(self, owner, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner = owner

    def save(self, commit=True):
        opportunity = super().save(commit=False)

        opportunity.owner = self.owner
        if commit:
            opportunity.save()
        # TO BE REMOVED IF NOT WORKING MANY2MANY
        self.save_m2m()

        return opportunity
    # end for additional changes

    class Meta:
        model = Opportunity
        exclude = ('owner', 'to_be_deleted', 'products', 'is_edite', 'newly_created')
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Opportunity name',
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Opportunity description',
                }
            ),
            'amount': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Opportunity amount',
                }
            ),
            'close_date': forms.TextInput(
                attrs={
                    'placeholder': 'Enter expected close date',
                }
            ),
        }
        labels = {
            'name': 'Opportunity Name',
        }

# OK
class CreateProductsOpportunityForm(forms.ModelForm):
    # as opportunity is hidden from the form to be populated should be updated init and save with owner
    def __init__(self, opportunity, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opportunity = opportunity

    def save(self, commit=True):
        products = super().save(commit=False)

        products.opportunity = self.opportunity
        if commit:
            products.save()
        # TO BE REMOVED IF NOT WORKING MANY2MANY
        # self.save_m2m()

        return products
    # end for additional changes

    class Meta:
        model = OpportunityProducts
        exclude = ('opportunity',)
        widgets = {
            'quantity': forms.TextInput(
                attrs={
                    'placeholder': 'Enter product quantity',
                }
            ),
        }
        labels = {
            'name': 'Product Name',
        }

#OK
class AddNewProductForm(forms.ModelForm):
    # as opportunity is hidden from the form to be populated should be updated init and save with owner
    def __init__(self, opportunity, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opportunity = opportunity

    def save(self, commit=True):
        products = super().save(commit=False)

        products.opportunity = self.opportunity
        name = self.cleaned_data['name']
        prod_id = Product.objects.get(name=name)
        if OpportunityProducts.objects.get(name_id=prod_id, opportunity_id=self.opportunity.pk):
            raise Exception('This Product was already included in the Opportunity')

        if commit:
            products.save()
        # TO BE REMOVED IF NOT WORKING MANY2MANY
        # self.save_m2m()

        return products
    # end for additional changes

    class Meta:
        model = OpportunityProducts
        exclude = ('opportunity',)
        widgets = {
            'quantity': forms.TextInput(
                attrs={
                    'placeholder': 'Enter product quantity',
                }
            ),
        }
        labels = {
            'name': 'Product Name',
        }

#OK
class CreateClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Client Name',
                }
            ),
            'city': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Client City',
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Client Email',
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Client Phone',
                }
            ),
            'discount': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Client Discount',
                }
            ),
        }
        labels = {
            'name': 'Client Name',
            'city': 'Client City',
            'email': 'Client Email',
            'phone': 'Client Phone',
        }


#OK
class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Product Name',
                }
            ),
            'price': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Product Price',
                }
            ),
        }
        labels = {
            'name': 'Product Name',
            'group': 'Product BusinessGroup',
            'price': 'Product Price',
        }


class CreateBusinessGroupForm(forms.ModelForm):
    class Meta:
        model = BusinessGroup
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter BusinessGroup Name',
                }
            ),
        }
        labels = {
            'name': 'Business Group Name',
        }
