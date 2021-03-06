from django.urls import path

from OpportunityManagementTool.web.views import HomeView, DashboardView, CreateOpportunityView, EditOpportunityView, \
    OpportunityDetailsView, CreateClientView, ClientDetailsView, EditClientView, ClientsListView, CreateProductView, \
    EditProductView, ProductsListView, CreateBusinessGroupView, EditBusinessGroupView, BusinessGroupsListView, \
    CreateProductsOpportunityView, EditOpportunityProductsView, OpportunityCreateOverView, done, AddNewProductView, \
    start_editing, finish_editing, OppProductsView, delete_opp, DeleteClientView, DeleteProductView, \
    ToBeDeletedOppsView, DeleteOpportunityView, DeleteOppProductView, ManagersListView

urlpatterns = (
    path('', HomeView.as_view(), name='index'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('opportunity/create/', CreateOpportunityView.as_view(), name='create opportunity'),
    path('opportunity/products/', CreateProductsOpportunityView.as_view(), name='products create opportunity'),
    path('opportunity/create/finalize/<int:pk>/',  OpportunityCreateOverView.as_view(), name='create opportunity finish'),
    path('done/<int:pk>/', done, name='done'),
    path('delete-opp/<int:pk>/', delete_opp, name='delete opp'),
    path('edit/start/<int:pk>/', start_editing, name='start edit'),
    path('edit/finish/<int:pk>/', finish_editing, name='finish edit'),
    path('opportunity/edit/<int:pk>/', EditOpportunityView.as_view(), name='edit opportunity'),
    path('opportunity/edit/product/<int:pk>/', EditOpportunityProductsView.as_view(), name='edit opportunity product'),
    path('opportunity/delete/product/<int:pk>/', DeleteOppProductView.as_view(), name='delete opportunity product'),
    path('opportunity/details/<int:pk>/', OpportunityDetailsView.as_view(), name='details opportunity'),
    path('opportunity/all/products/<int:pk>/', OppProductsView.as_view(), name='opportunity all products'),
    path('opportunity/products/new/', AddNewProductView.as_view(), name='opportunity new product add'),
    path('opportunities/tobedeleted/', ToBeDeletedOppsView.as_view(), name='opps to be deleted'),
    path('opportunity/delete/<int:pk>/', DeleteOpportunityView.as_view(), name='delete opportunity'),
    path('client/create/', CreateClientView.as_view(), name='create client'),
    path('client/edit/<int:pk>/', EditClientView.as_view(), name='edit client'),
    path('client/delete/<int:pk>/', DeleteClientView.as_view(), name='delete client'),
    path('client/details/<int:pk>/', ClientDetailsView.as_view(), name='details client'),
    path('clients/', ClientsListView.as_view(), name='clients catalog'),
    path('product/create/', CreateProductView.as_view(), name='create product'),
    path('product/edit/<int:pk>/', EditProductView.as_view(), name='edit product'),
    path('product/delete/<int:pk>/', DeleteProductView.as_view(), name='delete product'),
    path('products/', ProductsListView.as_view(), name='products catalog'),
    path('businessgroup/create/', CreateBusinessGroupView.as_view(), name='create businessgroup'),
    path('businessgroup/edit/<int:pk>/', EditBusinessGroupView.as_view(), name='edit businessgroup'),
    path('businessgroup/', BusinessGroupsListView.as_view(), name='businessgroup catalog'),
    path('managers/', ManagersListView.as_view(), name='managers catalog'),
)