from django.conf import settings
from django.contrib import messages
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
import json

# Mailchimp Settings
api_key = settings.MAILCHIMP_API_KEY
server = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID


def subscribe(request, email):
    """
    Contains code handling the communication to the mailchimp api
    to create a contact/member in an audience/list.
    """
    mailchimp = Client()
    mailchimp.set_config(
        {
            "api_key": api_key,
            "server": server,
        }
    )

    member_info = {
        "email_address": email,
        "status": "subscribed",
    }

    try:
        response = mailchimp.lists.add_list_member(list_id, member_info)
        if response:
            messages.success(request, "You have successfully subscribed. Thank you! ")
    except ApiClientError as error:
        json_error = json.loads(error.text)
        messages.error(request, f"Woops! {json_error['detail']}")
