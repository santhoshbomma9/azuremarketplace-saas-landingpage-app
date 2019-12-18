import uuid
import requests
from . import app_config
from . import constant


def get_subscriptionid_by_token(token):
    subscription_data = call_marketplace_api(constant.RESOLVE_ENDPOINT,
                                             request_method='POST',
                                             resolve_token=token)
    return subscription_data.json()


def get_subscription(subscription_id):
    subscription_data = call_marketplace_api(
        constant.GET_SUBSCRIPTION_ENDPOINT(subscription_id))
    return subscription_data


def get_availableplans(subscription_id):
    availableplans = call_marketplace_api(
        request_url=constant.GET_SUBSCRIPTION_PLANS(subscription_id))
    return availableplans


def get_marketplace_access_token():
    data = {'grant_type': 'client_credentials',
            'client_id': app_config.MARKETPLACEAPI_CLIENT_ID,
            'client_secret': app_config.MARKETPLACEAPI_CLIENT_SECRET, 
            'resource': app_config.MARKETPLACEAPI_RESOURCE}
    api_call_headers = {'content-type': 'application/x-www-form-urlencoded'}
    # get token for market place api
    access_token_response = requests.post(constant.MARKETPLACE_TOKEN_ENDPOINT,
                                          headers=api_call_headers,
                                          data=data).json()
    return access_token_response


def call_marketplace_api(request_url, request_method='GET', request_payload='', resolve_token=''):
    # get token for market place api
    access_token_response = get_marketplace_access_token()
    marketplaceheaders = {'Authorization': 'Bearer ' + access_token_response['access_token'],
                          'x-ms-marketplace-token': resolve_token,
                          'Content-Type': 'application/json',
                          'x-ms-requestid': str(uuid.uuid4()),
                          'x-ms-correlationid': str(uuid.uuid4())}

    if request_method == 'GET':
        response_data = requests.get(request_url,
                                     headers=marketplaceheaders).json()
        return response_data
    elif request_method == 'POST':
        response_data = requests.post(request_url,
                                      headers=marketplaceheaders,
                                      data=request_payload)
        return response_data
