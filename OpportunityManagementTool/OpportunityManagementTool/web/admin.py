from django.contrib import admin

from OpportunityManagementTool.web.models import BusinessGroup, Client, Opportunity, Product, OpportunityProducts


@admin.register(Client)
class ClientGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    pass


@admin.register(BusinessGroup)
class BusinessGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(OpportunityProducts)
class OpportunityProductsAdmin(admin.ModelAdmin):
    pass