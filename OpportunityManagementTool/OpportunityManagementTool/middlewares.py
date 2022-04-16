from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from OpportunityManagementTool.web.models import Opportunity


def handle_exception(get_response):
    def middleware(request):
        response = get_response(request)
        if response.status_code == 500:
            opportunity_edit = Opportunity.objects.get(is_edite=True)
            if "new" not in request.path_info.split('/'):
                return HttpResponseRedirect(request.path_info)
            return redirect('opportunity all products', opportunity_edit.pk)

        if response.status_code == 404 or response.status_code == 403:
            return redirect('index')
        return response

    return middleware
