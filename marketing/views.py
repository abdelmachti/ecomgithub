from django.conf import settings
from django.views import View
from django.http import  HttpResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView
from django.shortcuts import render, redirect

from .forms import  MarketingPreferenceForm
from .models import  MarketingPreference
from .utils import Mailchimp
from .mixins import CsrfExemptMixin

MAILCHIMP_EMAIL_LIST_ID = getattr(settings, "MAILCHIMP_EMAIL_LIST_ID", None)


class MarketingPreferenceUpdateView(SuccessMessageMixin, UpdateView):

    form_class = MarketingPreferenceForm
    template_name = 'base/forms.html' 
    success_url = '/settings/email/'
    success_message = "Your email preferences have been successfully changed!!!"

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            #return HttpResponse("not Allowed", status=400)
            return redirect("/login/?next=/settings/email/")
        return super(MarketingPreferenceUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(MarketingPreferenceUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Email Preferences'
        return context

    def get_object(self):
        user = self.request.user
        obj , created = MarketingPreference.objects.get_or_create(user=user)
        return obj

"""
METHOD is POST
---------------
"root":
"type": "subscribe"
"fired_at": "2020-05-04 01:38:47"
"data":
"id": "d1a643cf09"
"email": "amachti.de@gmail.com"
"email_type": "html"
"ip_opt": "77.0.200.120"
"web_id": "534691993"
"merges":
"EMAIL": "amachti.de@gmail.com"
"FNAME": "abdel"
"LNAME": "mach"
"ADDRESS": ""
"PHONE": ""
"BIRTHDAY": ""
"list_id": "48da2c2ea4"
"""

class MailchimpWebhookView(CsrfExemptMixin, View):
    def get(self, request,*args, **kwargs):
        return HttpResponse("Thanks for your Request", status=200)

    def post(self, request, *args, **kwargs):
        data = request.POST
        list_id = data.get('data[list_id]')
        if str(list_id)==str(MAILCHIMP_EMAIL_LIST_ID):
            hook_type = data.get('type')
            email = data.get('data[email]')
            response_status , response = Mailchimp().check_valid_status(email)
            sub_status = response['status'] 
            is_subbed = None
            mailchimp_subbed = None
            if sub_status == "subscribed":
                is_subbed , mailchimp_subbed =(True, True)
                """ qs = MarketingPreference.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(subscribed=True, mailchimp_subscribed=True, str(data)) """
            elif sub_status == "unsubscribed":
                is_subbed , mailchimp_subbed =(False, False)
                """ qs = MarketingPreference.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(subscribed=False, mailchimp_subscribed=False, str(data)) """
            if is_subbed is not None and mailchimp_subbed is not None:
                qs = MarketingPreference.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(
                                subscribed=is_subbed, 
                                mailchimp_subscribed=mailchimp_subbed,
                                mailchimp_msg=str(data)
                            )
        return HttpResponse ("Thank you!!!", status=200)


"""def mailchimp_webhook_view(request):
    data = request.POST
    list_id = data.get('data[list_id]')
    if str(list_id)==str(MAILCHIMP_EMAIL_LIST_ID):
        hook_type = data.get('type')
        email = data.get('data[email]')
        response_status , response = Mailchimp().check_valid_status(email)
        sub_status = response['status'] 
        is_subbed = None
        mailchimp_subbed = None
        if sub_status == "subscribed":
            is_subbed , mailchimp_subbed =(True, True)
            #qs = MarketingPreference.objects.filter(user__email__iexact=email)
            #if qs.exists():
                #s.update(subscribed=True, mailchimp_subscribed=True, str(data))
        elif sub_status == "unsubscribed":
            is_subbed , mailchimp_subbed =(False, False)
            #qs = MarketingPreference.objects.filter(user__email__iexact=email)
            #if qs.exists():
                #qs.update(subscribed=False, mailchimp_subscribed=False, str(data))
        if is_subbed is not None and mailchimp_subbed is not None:
            qs = MarketingPreference.objects.filter(user__email__iexact=email)
            if qs.exists():
                qs.update(
                            subscribed=is_subbed, 
                            mailchimp_subscribed=mailchimp_subbed,
                            mailchimp_msg=str(data)
                        )
    return HttpResponse ("Thank you!!!", status=200)"""
 


