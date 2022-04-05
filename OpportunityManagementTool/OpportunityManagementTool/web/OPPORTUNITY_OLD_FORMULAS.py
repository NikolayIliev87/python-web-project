# class CreateOpportunityForm(forms.ModelForm):
#     # as owner is hidden from the form to be populated should be updated init and save with owner
#     def __init__(self, owner, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.owner = owner
#
#     def save(self, commit=True):
#         opportunity = super().save(commit=False)
#
#         opportunity.owner = self.owner
#         if commit:
#             opportunity.save()
#         # TO BE REMOVED IF NOT WORKING MANY2MANY
#         self.save_m2m()
#
#         return opportunity
#     # end for additional changes
#
#     class Meta:
#         model = Opportunity
#         exclude = ('owner',)
#         widgets = {
#             'name': forms.TextInput(
#                 attrs={
#                     'placeholder': 'Enter Opportunity name',
#                 }
#             ),
#             'description': forms.TextInput(
#                 attrs={
#                     'placeholder': 'Enter Opportunity description',
#                 }
#             ),
#             'amount': forms.TextInput(
#                 attrs={
#                     'placeholder': 'Enter Opportunity amount',
#                 }
#             ),
#             'close_date': forms.TextInput(
#                 attrs={
#                     'placeholder': 'Enter expected close date',
#                 }
#             ),
#         }
#         labels = {
#             'name': 'Opportunity Name',
#         }
#
#
# class DashboardView(views.ListView):
#     model = Opportunity
#     template_name = 'web/dashboard.html'
#     context_object_name = "opportunities"
#
# # OK
# class CreateOpportunityView(auth_mixin.LoginRequiredMixin, views.CreateView):
#     form_class = CreateOpportunityForm
#     template_name = 'web/opportunity_create.html'
#     success_url = reverse_lazy('index')
#
#     # as owner is hidden from the form to be populated should be updated this method
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['owner'] = self.request.user
#         return kwargs
#
# # OK
# class OpportunityDetailsView(auth_mixin.LoginRequiredMixin, views.DetailView):
#     model = Opportunity
#     template_name = 'web/opportunity_details.html'
#     context_object_name = 'opportunity'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['is_owner'] = self.object.owner == self.request.user
#         # TO BE REMOVED IF NOT WORKING MANY2MANY
#         context['opp_products'] = self.object.product.all()
#
#         return context
#
# # OK
# class EditOpportunityView(views.UpdateView):
#     model = Opportunity
#     template_name = 'web/opportunity_edit.html'
#     fields = ('name', 'description', 'client', 'product', 'close_date')
#     success_url = reverse_lazy('dashboard')
#
# # TO BE CREATED
# class DeleteOpportunityView(views.DeleteView):
#     pass
#
#
#
# class Opportunity(models.Model):
#     NAME_MAX_LENGTH = 25
#     CLIENT_MAX_LENGTH = 20
#     PRODUCT_MAX_LENGTH = 30
#
#     WON = 'Won'
#     INPROGRESS = 'In Progress'
#     OPEN = 'Open'
#     LOST = 'Lost'
#
#     TYPES = [(x, x) for x in (WON, INPROGRESS, OPEN, LOST)]
#     TYPES_MAX_LENGTH = max([len(x) for x in (WON, INPROGRESS, OPEN, LOST)])
#
#     name = models.CharField(
#         max_length=NAME_MAX_LENGTH,
#         null=True,
#         blank=True,
#     )
#
#     def __str__(self):
#         return self.name
#
#     description = models.TextField(
#         null=True,
#         blank=True
#     )
#
#     client = models.ForeignKey(
#         Client,
#         on_delete=models.DO_NOTHING,
#         primary_key=False,
#         related_name='+',
#     )
#
#     product = models.ManyToManyField(
#         Product,
#     )
#
#     # product = models.ForeignKey(
#     #     Product,
#     #     on_delete=models.DO_NOTHING,
#     #     primary_key=False,
#     #     related_name='+',
#     # )
#
#     create_date = models.DateTimeField(
#         auto_now_add=True,
#     )
#
#     # amount = models.FloatField()
#
#     owner = models.ForeignKey(
#         UserModel,
#         on_delete=models.CASCADE,
#         primary_key=False,
#         related_name='+',
#     )
#
#     close_date = models.DateField()
#
#     status = models.CharField(
#         max_length=TYPES_MAX_LENGTH,
#         choices=TYPES,
#     )
#
#     @property
#     def final_price(self):
#         amount = sum([(i.price - (i.price * (self.client.discount/100))) for i in self.product.all()])
#
#         return amount
#
#     @property
#     def size_tire(self):
#         if self.final_price / 100 <= 0.1:
#             return "0-10K"
#         elif self.final_price / 100 <= 0.5:
#             return "10K=50K"
#         elif self.final_price / 100 <= 1.0:
#             return "50K-100K"
#         else:
#             return "Above 100K"