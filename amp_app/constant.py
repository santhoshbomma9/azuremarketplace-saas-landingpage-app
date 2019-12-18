from . import app_config

CUSTOMER_MANAGE_SUBSCRIPTION_PAGE = 'managesubscriptioncustomer.html'
ERROR_PAGE = 'error.html'
_404_PAGE = '404.html'
_500_PAGE = '500.HTML'

RESOLVE_ENDPOINT = f"{app_config.MARKETPLACEAPI_ENDPOINT}resolve{app_config.MARKETPLACEAPI_API_VERSION}"
MARKETPLACE_TOKEN_ENDPOINT = f"{app_config.AUTHORITY}{app_config.MARKETPLACEAPI_TENANTID}/oauth2/token"


def GET_SUBSCRIPTION_ENDPOINT(subscription_id):
    return f"{app_config.MARKETPLACEAPI_ENDPOINT}{subscription_id}{app_config.MARKETPLACEAPI_API_VERSION}"


def GET_SUBSCRIPTION_PLANS(subscription_id):
    return f"{app_config.MARKETPLACEAPI_ENDPOINT}{subscription_id}/listAvailablePlans{app_config.MARKETPLACEAPI_API_VERSION}"
