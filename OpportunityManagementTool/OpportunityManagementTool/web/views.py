from django.contrib.auth import mixins as auth_mixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views

from OpportunityManagementTool.web.forms import CreateOpportunityForm, CreateClientForm, CreateProductForm, \
    CreateBusinessGroupForm, CreateProductsOpportunityForm, AddNewProductForm
from OpportunityManagementTool.web.models import Opportunity, Client, Product, BusinessGroup, OpportunityProducts


# OK
class HomeView(views.TemplateView):
    template_name = 'web/home_page_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


# OK
class DashboardView(auth_mixin.LoginRequiredMixin, views.ListView):
    model = Opportunity
    template_name = 'web/dashboard.html'
    context_object_name = "opportunities"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        opp_gross_amount = {}
        opp_num = 0
        opps_total = 0

        for el in Opportunity.objects.filter(to_be_deleted=False):
            if el.owner == self.request.user or el.owner.manager == self.request.user.id:
                for prod in OpportunityProducts.objects.all():
                    if el.id == prod.opportunity_id:
                        if el.id in opp_gross_amount:
                            opp_gross_amount[el.id] += prod.gross_price
                            opps_total += prod.gross_price
                        else:
                            opp_gross_amount[el.id] = prod.gross_price
                            opps_total += prod.gross_price
                opp_num += 1

        context['opportunities_product_id'] = OpportunityProducts.objects.all()
        context['opp_gross_amount'] = opp_gross_amount
        context['opp_num'] = opp_num
        context['opps_total'] = opps_total
        try:
            in_creation_mode = Opportunity.objects.get(is_edite=True, owner=self.request.user)
            if in_creation_mode:
                context['in_edit_mode'] = in_creation_mode
                return context
        except:
            return context

        # return context
    def get_queryset(self):
        return Opportunity.objects.filter(to_be_deleted=False)


# OK
class ToBeDeletedOppsView(auth_mixin.LoginRequiredMixin, views.ListView):
    model = Opportunity
    template_name = 'web/to_be_deleted_opportunities_list.html'
    context_object_name = "opportunities"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        return super(ToBeDeletedOppsView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Opportunity.objects.filter(to_be_deleted=True)


# OK
class CreateOpportunityView(auth_mixin.LoginRequiredMixin, views.CreateView):
    form_class = CreateOpportunityForm
    template_name = 'web/opportunity_create.html'
    success_url = reverse_lazy('products create opportunity')

    # as owner is hidden from the form to be populated should be updated this method
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs

    # check if there is opportunity which should be finalized
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            in_creation_mode = Opportunity.objects.get(newly_created=True, owner=self.request.user)
            if in_creation_mode:
                context['in_creation_mode'] = in_creation_mode
                return context
        except:
            return context


# OK
class CreateProductsOpportunityView(auth_mixin.LoginRequiredMixin, views.CreateView):
    form_class = CreateProductsOpportunityForm
    template_name = 'web/opportunity_create_products.html'
    success_url = reverse_lazy('products create opportunity')

    def get_context_data(self, **kwargs):
        opp_id = Opportunity.objects.get(newly_created=True, owner=self.request.user)
        context = super().get_context_data(**kwargs)
        context['opportunity'] = opp_id
        context['product_id'] = OpportunityProducts.objects.filter(opportunity_id=opp_id)
        return context

    # as opportunity is hidden from the form to be populated should be updated this method
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['opportunity'] = Opportunity.objects.get(newly_created=True)
        return kwargs


# OK
def done(request, pk):
    opp = Opportunity.objects.get(pk=pk)
    opp.newly_created = False
    opp.save()
    return redirect('index')


def start_editing(request, pk):
    opp = Opportunity.objects.get(pk=pk)
    opp.is_edite = True
    opp.save()
    return redirect('edit opportunity', pk)


def finish_editing(request, pk):
    opp = Opportunity.objects.get(pk=pk)
    opp.is_edite = False
    opp.save()
    return redirect('details opportunity', pk)


def delete_opp(request, pk):
    opp = Opportunity.objects.get(pk=pk)
    opp.to_be_deleted = True
    opp.save()
    return redirect('dashboard')


# OK
class OpportunityCreateOverView(views.DetailView):
    model = Opportunity
    template_name = 'web/opportunity_create_overview.html'
    context_object_name = 'opportunity'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['opp_products'] = OpportunityProducts.objects.filter(opportunity_id=self.object.pk)
        return context


# OK
class OpportunityDetailsView(auth_mixin.LoginRequiredMixin, views.DetailView):
    model = Opportunity
    template_name = 'web/opportunity_details.html'
    context_object_name = 'opportunity'

    def get_queryset(self):
        return Opportunity.objects.filter(owner_id=self.request.user.pk)

    def get_context_data(self, **kwargs):
        opp_products = self.object.products.all()
        product_id = OpportunityProducts.objects.filter(opportunity_id=self.object.pk)
        total_value = 0
        for opp in opp_products:
            for prod in product_id:
                if opp.id == prod.name_id:
                    total_value += prod.quantity * opp.price
        discount = total_value * (self.object.client.discount / 100)
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.owner == self.request.user
        context['opp_products'] = opp_products
        context['total_value'] = total_value
        context['discount'] = discount
        context['product_id'] = product_id
        return context


# OK
class EditOpportunityView(views.UpdateView):
    model = Opportunity
    template_name = 'web/opportunity_edit.html'
    fields = ('name', 'description', 'client', 'close_date')

    def get_queryset(self):
        return Opportunity.objects.filter(owner_id=self.request.user.pk)

    def get_success_url(self):
        # products_id = OpportunityProducts.objects.get(opportunity_id=self.object.pk)
        return reverse_lazy('opportunity all products', kwargs={'pk': self.object.pk})
        # return reverse_lazy('edit opportunity products', kwargs={'pk': products_id.pk})


# OK
class OppProductsView(auth_mixin.LoginRequiredMixin, views.DetailView):
    model = Opportunity
    template_name = 'web/opportunity_all_products.html'
    context_object_name = "opportunity"

    def get_queryset(self):
        return Opportunity.objects.filter(owner_id=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.owner == self.request.user
        context['opp_products'] = self.object.products.all()
        context['product_id'] = OpportunityProducts.objects.filter(opportunity_id=self.object.pk)
        return context


# OK
class EditOpportunityProductsView(views.UpdateView):
    model = OpportunityProducts
    template_name = 'web/opportunity_edit_products.html'
    fields = ('name', 'quantity',)

    def get_success_url(self):
        return reverse_lazy('opportunity all products', kwargs={'pk': self.object.opportunity_id})


# OK
class AddNewProductView(auth_mixin.LoginRequiredMixin, views.CreateView):
    form_class = AddNewProductForm
    template_name = 'web/opportunity_add_product.html'

    def get_success_url(self):
        product = OpportunityProducts.objects.get(pk=self.object.pk).opportunity_id
        return reverse_lazy('opportunity all products', kwargs={'pk': product})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['opportunity'] = Opportunity.objects.get(is_edite=True)
        return kwargs


# OK
class DeleteOpportunityView(views.DeleteView):
    model = Opportunity
    template_name = 'web/opportunity_delete_list.html'
    success_url = reverse_lazy('opps to be deleted')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        success_url = self.get_success_url()
        self.object.delete()

        return HttpResponseRedirect(success_url)


# OK
class CreateClientView(auth_mixin.LoginRequiredMixin, views.CreateView):
    form_class = CreateClientForm
    template_name = 'web/client_create.html'
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            return super(CreateClientView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()



# OK
class ClientDetailsView(auth_mixin.LoginRequiredMixin, views.DetailView):
    model = Client
    template_name = 'web/client_details.html'
    context_object_name = 'client'


# OK
class EditClientView(views.UpdateView):
    model = Client
    template_name = 'web/client_edit.html'
    fields = ('name', 'city', 'email', 'phone', 'discount',)
    success_url = reverse_lazy('clients catalog')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            return super(EditClientView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()


# OK
class ClientsListView(views.ListView):
    model = Client
    template_name = 'web/clients_list.html'
    context_object_name = "clients"


# OK
class DeleteClientView(views.DeleteView):
    model = Client
    template_name = 'web/client_delete.html'
    success_url = reverse_lazy('clients catalog')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        return super(DeleteClientView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        for opp in Opportunity.objects.filter(client=self.object):
            opp.delete()
        success_url = self.get_success_url()
        self.object.delete()

        return HttpResponseRedirect(success_url)


class CreateProductView(auth_mixin.LoginRequiredMixin, views.CreateView):
    form_class = CreateProductForm
    template_name = 'web/product_create.html'
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        return super(CreateProductView, self).dispatch(request, *args, **kwargs)


# OK
class EditProductView(views.UpdateView):
    model = Product
    template_name = 'web/product_edit.html'
    fields = ('name', 'group', 'price',)
    success_url = reverse_lazy('products catalog')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        return super(EditProductView, self).dispatch(request, *args, **kwargs)


# OK
class ProductsListView(views.ListView):
    model = Product
    template_name = 'web/products_list.html'
    context_object_name = "products"


# Ok
class DeleteProductView(views.DeleteView):
    model = Product
    template_name = 'web/product_delete.html'
    success_url = reverse_lazy('products catalog')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        return super(DeleteProductView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        for prod in OpportunityProducts.objects.filter(name_id=self.object):
            prod.delete()
        success_url = self.get_success_url()
        self.object.delete()

        return HttpResponseRedirect(success_url)


# Ok
class CreateBusinessGroupView(auth_mixin.LoginRequiredMixin, views.CreateView):
    form_class = CreateBusinessGroupForm
    template_name = 'web/business_group_create.html'
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        return super(CreateBusinessGroupView, self).dispatch(request, *args, **kwargs)


# OK
class EditBusinessGroupView(views.UpdateView):
    model = BusinessGroup
    template_name = 'web/business_group_edit.html'
    fields = ('name',)
    success_url = reverse_lazy('businessgroup catalog')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        return super(EditBusinessGroupView, self).dispatch(request, *args, **kwargs)


# OK
class BusinessGroupsListView(views.ListView):
    model = BusinessGroup
    template_name = 'web/business_group_list.html'
    context_object_name = "businessgroups"

