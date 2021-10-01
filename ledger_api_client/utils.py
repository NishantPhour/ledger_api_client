from django.core.exceptions import ValidationError
from django.conf import settings
import django
import requests
import json 

def oracle_parser(): 
    pass

def update_payments():
    pass

def create_basket_session(request, emailuser_id, parameters):
    # emailuser_id use to be request vairable.  This has been 
    # replaced with the user objects.  You will need to change 
    #request to request.user.id for this function
    payment_session = None
    cookies = None 
    if 'payment_session' in request.session:
          payment_session = request.session.get('payment_session')
          cookies = {'sessionid': payment_session}

    api_key = settings.LEDGER_API_KEY
    url = settings.LEDGER_API_URL+'/ledgergw/remote/create-basket-session/'+api_key+'/'
    myobj = {'parameters': json.dumps(parameters), 'emailuser_id': emailuser_id,}
   
    try:
        # send request to server to get file
        resp = requests.post(url, data = myobj, cookies=cookies)
    except Exception as e:
         raise ValidationError('Error: Unable to create basket session - unable to connect to payment gateway')        

    if int(resp.json()['status']) == 200:

         for c in resp.cookies:
              if c.name ==  'sessionid':
                  request.session['payment_session'] = c.value
         request.session['basket_hash'] = resp.json()['data']['basket_hash']
         return resp.json()['data']['basket_hash']
    else:
        raise ValidationError('Error: Unable to create basket session ') 

def create_checkout_session(request, checkout_parameters):

    django_version = float(str(django.VERSION[0])+'.'+str(django.VERSION[1]))

    checkout_parameters['user_logged_in'] = None
    is_authen = False
    if django_version > 1.11:
          is_authen = request.user.is_authenticated
    else: 
          is_authen = request.user.is_authenticated()
    if is_authen:
           checkout_parameters['user_logged_in'] = request.user.id

    api_key = settings.LEDGER_API_KEY
    url = settings.LEDGER_API_URL+'/ledgergw/remote/create-checkout-session/'+api_key+'/'
    myobj = {'checkout_parameters': json.dumps(checkout_parameters),}

    cookies = {}
    if 'payment_session' in request.session:
        payment_session = request.session.get('payment_session')
        cookies = {'sessionid': payment_session}
    session = requests.Session()
    try:
        # send request to server to get file
        resp = requests.post(url, data = myobj, cookies=cookies)
    except Exception as e:
         raise ValidationError('Error: Unable to create basket session - unable to connect to payment gateway')


    if int(resp.json()['status']) == 200:
        for c in resp.cookies:
            if c.name ==  'sessionid':
                 request.session['payment_session'] = c.value
    else:
        raise ValidationError('Error: Unable to create checkout session ')    
        
def payment_details_checkout(request):
    pass
#/ledger/checkout/checkout/payment-details/


def place_order_submission():
    pass


def use_existing_basket():
    pass

def use_existing_basket_from_invoice():
    pass

def get_invoice_properties(invoice_id):
    print ("G1")
    api_key = settings.LEDGER_API_KEY
    url = settings.LEDGER_API_URL+'/ledgergw/remote/get-invoice/'+api_key+'/'
    myobj = {'data': json.dumps({'invoice_id': invoice_id})}
    cookies = {}
    resp = requests.post(url, data = myobj, cookies=cookies)
    print ("G2")
    #print (resp.text)
    return resp.json()

class OrderObject():
     def __init__(self):
           self.id = None
           self.number = None
           

class Order:
     class objects:
         def get(**kwargs):
             api_key = settings.LEDGER_API_KEY
             url = settings.LEDGER_API_URL+'/ledgergw/remote/get_order_info/'+api_key+'/'
             myobj = {'data': json.dumps(kwargs)}
             cookies = {}
             session = requests.Session()
             # send request to server to get file
             resp = requests.post(url, data = myobj, cookies=cookies)
             print (resp)            
             print (resp.text)
             o = OrderObject()
             o.id = resp.json()['data']['order']['id']
             o.number = resp.json()['data']['order']['number']

             return o 
