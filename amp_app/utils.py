import msal
from flask import session
from . import app_config


def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache


def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()


def _build_msal_app(cache=None):
    return msal.ConfidentialClientApplication(
        app_config.CLIENT_ID,
        authority=app_config.AUTHORITY + "common",
        client_credential=app_config.CLIENT_SECRET,
        token_cache=cache)


def _get_token_from_cache(scope=None):
    cache = _load_cache()  # This web app maintains one cache per session
    cca = _build_msal_app(cache=cache)
    accounts = cca.get_accounts()
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(cache)
        return result


def _get_activate_email_body(subscription):
    email_body = "<table border='1' cellpadding='5' cellspacing='0' id='emailHeader'>"
    for key in subscription:
        email_body += ("<tr><td align='center' valign='top'>" + str(key) + "</td>"
                       "<td valign='top'>" + str(subscription.get(key)) + "</td></tr>")
    email_body += "</table><br>"
    print(email_body)
    return email_body


def _get_update_email_body(subscription, to_plan):
    email_body = "<table border='1' cellpadding='5' cellspacing='0' id='emailHeader'>"
    for key in subscription:
        email_body += ("<tr><td align='center' valign='top'>" + str(key) + "</td>"
                       "<td valign='top'>" + str(subscription.get(key)) + "</td></tr>")
        email_body += ("<tr><td align='center' valign='top'>Upgrade To Plan</td>"
                       "<td valign='top'>" + str(to_plan) + "</td></tr>")
    email_body += "</table><br>"
    print(email_body)
    return email_body
