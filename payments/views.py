from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework import mixins, viewsets, views
from rest_framework.decorators import action
from rest_framework import filters, permissions, response
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from urllib.parse import urlencode
from rest_framework import status
from rest_framework.parsers import JSONParser
from payments.models import Order, Ledger, PaymentArchive
from jobs.models import Job
import requests
import json

class PaymentsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]

    @action(methods=['post'], detail=False, url_name='initiate-payment', url_path='initiate/sslcommerz')
    def initiate_payment(self, request):
        sslcommerz_init_payment_url = 'https://sandbox.sslcommerz.com/gwprocess/v4/api.php'
        print(request.data)
        if not request.data.get('product_id', None):
           return response.Response({'message': 'invalirsatarstd'}, status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.create(product_reference_id=request.data['product_id'], amount="150.00", user=request.user, currency="BDT", type="JOB_POSTING")
        store_id = '***REMOVED***'
        store_passwd = '***REMOVED***'
        environ = 'https://www.worklist.club/'
        user = request.user
        success_url = environ + 'payments/successful/'
        fail_url = environ + 'payments/failed/'
        cancel_url = environ + 'payments/cancelled/'
        ipn_url = environ + 'https://webhook-test.com/ef6a1396c9cb8f3876a55b9508b58a92'
        cus_email = user.email
        cus_name = 'Aryan'
        data = {
            'cus_email': cus_email,
            'cus_name': cus_name,
            'cus_add1': '',
            'cus_city': '',
            'cus_country': '',
            'cus_phone': '+8801761443969',
            'shipping_method': 'NO',
            'sessionkey': order.id,
            'emi_option': 0,
            'product_name': 'WorkList Job Listing',
            'product_category': 'general',
            'product_profile': 'non-physical-goods',
            'user': user.id,
        }
        body = {
                'store_id': store_id,
                'store_passwd': store_passwd,
                'success_url': 'https://c016-103-197-153-66.ngrok-free.app/payments/notifications/sslcommerz/',
                'fail_url': fail_url,
                'cancel_url': cancel_url,
                'ipn_url': 'https://c016-103-197-153-66.ngrok-free.app/payments/notifications/sslcommerz/',
                **data,
                'tran_id': order.id,
                'total_amount': order.amount
            }
        ssl_response = requests.post(sslcommerz_init_payment_url, data=urlencode(body), headers={'Content-Type': 'application/x-www-form-urlencoded'})
        return response.Response(ssl_response.json())
    
    @action(methods=['post'], detail=False, permission_classes=[permissions.AllowAny], url_name='payment', url_path='notifications/sslcommerz')
    def confirm_payment(self, request):
        request_okay = request.data['status'] == 'VALID' and request.data['risk_level'] == '0' and request.data['risk_title'] == 'Safe' and request.data['amount'] == '150.00' and request.data['currency'] == 'BDT'
        print(request_okay, request.data['status'] == 'VALID', request.data['risk_level'] == '0', request.data['risk_title'] == 'Safe', request.data['amount'] == '150.00', request.data['currency'] == 'BDT')
        print(request.data)
        if request_okay:
            order = Order.objects.get(pk=request.data['tran_id'])
            job = Job.jobs.get(pk=order.product_reference_id)
            print(job.online_until)
            res = requests.get(f'https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php?val_id={request.data["val_id"]}&store_id=***REMOVED***&store_passwd=***REMOVED***%40ssl&format=json')
            PaymentArchive.objects.create(data=res.text, order=order)
            parsed = res.json()
            if parsed['status'] == 'VALID':
                Ledger.objects.create(user=order.user, type='DEBIT', amount=order.amount, currency=order.currency, order=order)
                job.publish_job()
                print(job.online_until)
        else:
            print(request)
        return response.Response({'message': 'invalid'}, status=status.HTTP_400_BAD_REQUEST)
