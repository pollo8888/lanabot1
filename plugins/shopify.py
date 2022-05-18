import time 
import requests
from rand_user import random_user_api

rand_user = random_user_api().get_random_user_info()
from random_address import real_random_address

addr = real_random_address()


def find_between( data, first, last ):
    try:
        start = data.index( first ) + len( first )
        end = data.index( last, start )
        return data[start:end]
    except ValueError:
        return None


r = requests.Session()


cc = "5424181422031026"
mes = "02"
ano = 2023
cvv = "981"



def one_def(r):
    a= r.get('https://www.rabitat.com/collections/squeezy-bottles/products/snap-lock-sipper-bottle-410ml')

    varient_id = find_between(a.text, 'variantId":',',')

    if not a or not varient_id:
        return 

    b = r.post('https://www.rabitat.com/cart/add.js', headers = {'x-requested-with': 'XMLHttpRequest'},data = 'items%5B0%5D%5Bquantity%5D=1&items%5B0%5D%5Bid%5D=40858600308915&items%5B0%5D%5Bproperties%5D%5BProduct+Name%5D=Snap+Lock+Sipper+Bottle+(410ml)')

    if not b:
        return

    c = r.post('https://www.rabitat.com/cart/add.js', headers = {'x-requested-with': 'XMLHttpRequest'},data = 'Color=true&form_type=product&utf8=%E2%9C%93&Color=undefined&Color=Young%20wild%20and%20free-%20Hoping%20to%20raise%20a%20free%20spirit%3F%20Start%20with%20her%20first%20interaction%20with%20the%20world%2C%20the%20colours%20will%20help%20your%20darling%E2%80%99s%20brain%20development%20and%20we%20all%20know%20that%20will%20make%20her%20think%20and%20make%20her%20the%20spirited%20thinker%20you%20dreaming%20of.%20Amen&id=31600488939609')

    if not c:
        return

# print(b.status_code, c.status_code) 200

    d = r.post('https://www.rabitat.com/cart', headers = {'x-requested-with': 'XMLHttpRequest'},data = 'updates%5B%5D=1&updates%5B%5D=1&rbfeature_discount=defaultetxtbox&coupon_discount=&checkout=')

# print(d.status_code, d.url) 200
    auth_token = find_between(d.text, 'type="hidden" name="authenticity_token" value="','"')

    if not d or not auth_token:
        return

    checkout_url = d.url
    return auth_token,checkout_url




def two_def(rand_user, addr, r, auth_token, checkout_url):
    dic = {
'_method': 'patch',
'authenticity_token': auth_token,
'previous_step': 'contact_information',
'step': 'shipping_method',
'checkout[email]': rand_user.email,
'checkout[buyer_accepts_marketing]': '0',
'checkout[shipping_address][first_name]': rand_user.first_name,
'checkout[shipping_address][last_name]': rand_user.last_name,
'checkout[shipping_address][address1]': addr['address1'],
'checkout[shipping_address][address2]': '',
'checkout[shipping_address][city]': addr['city'],
'checkout[shipping_address][country]': 'United States',
'checkout[shipping_address][province]': addr['state'],
'checkout[shipping_address][zip]': addr['postalCode'],
'checkout[shipping_address][phone]': rand_user.phone,
'checkout[remember_me]': '',
'checkout[remember_me]': '0',
'checkout[client_details][browser_width]': '796',
'checkout[client_details][browser_height]': '627',
'checkout[client_details][javascript_enabled]': '1',
'checkout[client_details][color_depth]': '24',
'checkout[client_details][java_enabled]': 'false',
'checkout[client_details][browser_tz]': '-330',
}


    e = r.post(checkout_url, data = dic)

    shoping_id = find_between(e.text, '<div class="radio-wrapper" data-shipping-method="','"')

    # print(e.url, e.status_code)
    # with open('a.txt', 'w') as w: w.write(e.text)
    if not e or not shoping_id:
        return

    dic = {
'_method': 'patch',
'authenticity_token': auth_token,
'previous_step': 'shipping_method',
'step': 'payment_method',
'checkout[shipping_rate][id]': shoping_id,
'checkout[client_details][browser_width]': '811',
'checkout[client_details][browser_height]': '627',
'checkout[client_details][javascript_enabled]': '1',
'checkout[client_details][color_depth]': '24',
'checkout[client_details][java_enabled]': 'false',
'checkout[client_details][browser_tz]': '-330',
}


    f = r.post(checkout_url, data = dic)

    # with open('f.txt', 'w') as w: w.write(f.text)
    price  = find_between(f.text,'input type="hidden" name="checkout[total_price]" id="checkout_total_price" value="','"')

    payment_gateway = find_between(f.text,'data-subfields-for-gateway="','"')
    if not f or not payment_gateway:
        return
    # print(f.url, f.status_code) 

    return price,payment_gateway


def def_last(rand_user, r, cc, mes, ano, cvv, auth_token, checkout_url, price, payment_gateway):
    json_four = {
    "credit_card": {
        "number": cc,
        "name": rand_user.name,
        "month": mes,
        "year": ano,
        "verification_value": cvv
    },
    "payment_session_scope": "www.rabitat.com"
}

    four = r.post('https://deposit.us.shopifycs.com/sessions', json = json_four)

# print(four.text, four.status_code) 200
    if 'id' not in four.json():
        return


    dic = {
'_method': 'patch',
'authenticity_token': auth_token,
'previous_step': 'payment_method',
'step': '',
's': four.json()['id'],
'checkout[payment_gateway]': payment_gateway,
'checkout[credit_card][vault]': 'false',
'checkout[different_billing_address]': 'false',
'checkout[total_price]': price,
'complete': '1',
'checkout[client_details][browser_width]': '796',
'checkout[client_details][browser_height]': '627',
'checkout[client_details][javascript_enabled]': '1',
'checkout[client_details][color_depth]': '24',
'checkout[client_details][java_enabled]': 'false',
'checkout[client_details][browser_tz]': '-330',
}
    
    f = r.post(checkout_url, data = dic)
    

    if not f or 'processing' not in f.url:
        return 
    time.sleep(5)

    g = r.get(checkout_url + '/processing?from_processing_page=1', allow_redirects = True)
        
    if 'from_processing_page=1&validate=true' not in g.url:
        h = r.get(g.url, allow_redirects= True)
        link = find_between(h.text,'<a href="','"')
        if not h or not link : return
        i = r.get(link)
        if not i: return

        # with open('m.txt', 'w') as w: w.write(h.text)


    time.sleep(4)
    i = r.get(checkout_url + '?from_processing_page=1&validate=true', allow_redirects= True)
    if not i:
        return
    return i