from django.shortcuts import redirect
from django.views.generic import RedirectView

from marketing.utils import subscribe


class SubscriptionView(RedirectView):
    """
    Class to handle subscription requests
    """

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            currentpath = request.POST.get("currentpath")
            email = request.POST["email"]
            subscribe(request, email)

        return redirect(currentpath, *args, **kwargs)
