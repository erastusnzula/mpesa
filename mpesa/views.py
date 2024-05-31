import json

from django.shortcuts import render
from django.views import View
from requests.auth import HTTPBasicAuth
from django.conf import settings
from django.http import JsonResponse
import base64
from datetime import datetime
import requests
from .models import STKPushTransaction


def get_access_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"\
        if settings.MPESA_ENVIRONMENT == 'sandbox' \
        else "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    response.raise_for_status()
    access_token= response.json().get('access_token')
    return access_token


def initiate_stk_push(mobile_number, amount, reference, description):
    access_token = get_access_token()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"\
        if settings.MPESA_ENVIRONMENT == 'sandbox' \
        else "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    initiation_time = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(
        (settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + initiation_time).encode('utf-8')).decode('utf-8')
    data = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": initiation_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": mobile_number,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": mobile_number,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": reference,
        "TransactionDesc": description
    }

    response = requests.post(api_url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()


class STKPush(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'stk_push.html')

    def post(self, *args, **kwargs):
        mobile_number = int(self.request.POST.get('mobile_number'))
        amount = int(self.request.POST.get('amount'))
        reference = self.request.POST.get('reference')
        description = self.request.POST.get('description')
        response = initiate_stk_push(mobile_number=mobile_number, amount=amount, reference=reference,
                                     description=description)
        return JsonResponse(response)


class CallBack(View):
    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        stk_push_transaction = STKPushTransaction()
        stk_push_transaction.merchant_id = data['Body']['stkCallback']['MerchantRequestID'],
        stk_push_transaction.checkout_id = data['Body']['stkCallback']['CheckoutRequestID'],
        stk_push_transaction.transaction_date = data['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value'],
        stk_push_transaction.reference = data['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value'],
        stk_push_transaction.result_code = data['Body']['stkCallback']['ResultCode'],
        stk_push_transaction.result_description = data['Body']['stkCallback']['ResultDesc'],
        stk_push_transaction.mobile_number = data['Body']['stkCallback']['CallbackMetadata']['Item'][4]['Value']
        stk_push_transaction.amount = data['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value'],
        stk_push_transaction.balance = data['Body']['stkCallback']['CallbackMetadata']['Item'][2]['Value'],
        print(data)
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
