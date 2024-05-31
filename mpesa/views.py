import json
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import STKPushTransaction
from .utils import initiate_stk_push


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
