from flask import (redirect, render_template, request, session, url_for, flash, abort)
from flask_session import Session
from . import amprepo, app_config, constant, utils, app
from functools import wraps
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import logging
import uuid

app.config.from_object(app_config)
Session(app)
requested_url = ''


# -----------------------------------------------------------
# Implement Gunicorn logging
# https://medium.com/@trstringer/logging-flask-and-gunicorn-the-manageable-way-2e6f0b8beb2f
# -----------------------------------------------------------
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


# -----------------------------------------------------------
# Login Decorator
# -----------------------------------------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        app.logger.error('login_required '+request.url)
        if not session.get("user"):
            global requested_url
            app.logger.error('login_required '+requested_url)
            requested_url = request.url
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# -----------------------------------------------------------
# 404 page handler
# -----------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    if session.get("user"):
        return render_template(constant._404_PAGE, user=session["user"]), 404
    else:
        return render_template(constant._404_UNAUTH_PAGE), 404


# -----------------------------------------------------------
# 500 page handler
# -----------------------------------------------------------
@app.errorhandler(500)
def internal_error(e):
    return render_template(constant._500_PAGE), 500


# -----------------------------------------------------------
# Login page redirect - makes sure the user is logged in
# -----------------------------------------------------------
@app.route("/")
def login():
    if not session.get("user"):
        session["state"] = str(uuid.uuid4())
        auth_url = utils._build_msal_app().get_authorization_request_url(
                        [],
                        state=session["state"],
                        redirect_uri=url_for("authorized",
                                             _external=True,
                                             _scheme=app_config.HTTP_SCHEME))
        return redirect(auth_url, code=302)
    else:
        global requested_url
        app.logger.error('login '+requested_url)
        if not requested_url:
            abort(404)
        return redirect(requested_url)


# -------------------------------------------------------------------------
# Redirect/callback path, when the login is succesful validated by Azure AD
# -------------------------------------------------------------------------
@app.route(app_config.REDIRECT_PATH)
def authorized():
    if request.args.get('state') == session.get("state"):
        cache = utils._load_cache()
        result = utils._build_msal_app(cache=cache).acquire_token_by_authorization_code(
            request.args['code'],
            scopes=[],  # Misspelled scope would cause an HTTP 400 error here
            redirect_uri=url_for("authorized",
                                 _external=True,
                                 _scheme=app_config.HTTP_SCHEME))
        if "error" in result:
            return "Login failure: %s, %s" % (
                result["error"], result.get("error_description"))
        session["user"] = result.get("id_token_claims")
        utils._save_cache(cache)
    return redirect(url_for("login"))


# --------------------------------------------------------------------
# Landing page
# --------------------------------------------------------------------
@app.route("/landingpage", methods=['GET', 'POST'])
@login_required
def landingpage():
    global requested_url
    app.logger.error('landingpage '+requested_url)
    requested_url = ''
    token = request.args.get('token')
    subscription = amprepo.get_subscriptionid_by_token(token)
    if not token or 'id' not in subscription:
        return render_template(constant.ERROR_PAGE, user=session["user"])
    subscription_data = amprepo.get_subscription(subscription['id'])
    plans = amprepo.get_availableplans(subscription['id'])

    if request.method == 'POST':
        subject = ''
        email_body = ''
        id_string = 'id'
        if 'activate' in request.form:
            selected_plan = request.form['subscription_plan_id']
            subject = f'New activation request for Subscription {subscription_data.get(id_string)}'
            email_body = utils._get_activate_email_body(subscription_data)
        elif 'update' in request.form:
            selected_plan = request.form['selectedplan']
            subject = f'UPDATE request for Subscription \
                        {subscription_data.get(id_string)}'
            email_body = utils._get_update_email_body(subscription_data,
                                                      selected_plan)

        email_body += "<br> Go to <a href="+url_for('login', _external=True)+">Dashboard</a>"

        message = Mail(
            from_email=app_config.SENDGRID_FROM_EMAIL,
            to_emails=app_config.SENDGRID_TO_EMAIL,
            subject=subject,
            html_content=email_body)
        try:
            sendgrid_client = SendGridAPIClient(app_config.SENDGRID_APIKEY)
            response = sendgrid_client.send(message)
            flash(f'{response.status_code} Message sent successfully')
        except Exception as e:
            flash(e.message, 'error')

    return render_template(constant.CUSTOMER_MANAGE_SUBSCRIPTION_PAGE,
                           user=session["user"],
                           subscription=subscription_data,
                           available_plans=plans)


@app.route("/support", methods=['GET', 'POST'])
@login_required
def support():
    global requested_url
    app.logger.error('support '+requested_url)
    requested_url = ''
    if request.method == 'POST':
        replyEmail = request.form['email']
        question = request.form['message']

        message = Mail(
            from_email=app_config.SENDGRID_FROM_EMAIL,
            to_emails=app_config.SENDGRID_TO_EMAIL,
            subject='Sending with Twilio SendGrid is Fun',
            html_content=f'<strong>and easy {question}  {replyEmail} to do \
                            anywhere, even with Python</strong>')
        try:
            sendgrid_client = SendGridAPIClient(app_config.SENDGRID_APIKEY)
            response = sendgrid_client.send(message)
            flash(f'{response.status_code} Message sent successfully')
        except Exception as e:
            flash(e.message, 'error')

    return render_template('support.html', user=session["user"])


@app.route("/logout")
def logout():
    session.clear()  # Wipe out user and its token cache from session
    return redirect(  # Also logout from your tenant's web session
        # app_config.AUTHORITY + "/" + app_config.TENANT_ID + "/oauth2/v2.0/logout" +
        app_config.AUTHORITY + "/common/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("login",
                                               _external=True,
                                               _scheme=app_config.HTTP_SCHEME))
