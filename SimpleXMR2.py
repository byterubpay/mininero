import MiniNero
import os
import ed25519
import binascii
import PaperWallet

import json, hmac, hashlib, time, requests

#gets btr address, btr amount, and pid for btr2 order
#inputs are btc destination, and amount in btc
#also will return the order id, so you can track the order
def btc2btr(dest, amount):
    #First create the order..
    url = 'https://btr.to/api/v1/btr2btc/order_create/'   
    payload = {'btc_dest_address' : dest, 'btc_amount' : amount}
    headers = {'content-type': 'application/json'}   
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    data = json.loads(r.content)
    uuid = data['uuid']
    print("uuid=", uuid)
    
    #wait a few seconds 
    print("waiting a few seconds for order to be created")
    for i in range(0, 5):
        print(".")
        time.sleep(1)    
        
    #get amount, address, pid
    ipStatus = 'https://btr.to/api/v1/btr2btc/order_status_query/'
    dat = {
        'uuid' : uuid
        }
    r2 = requests.post(ipStatus, data=json.dumps(dat), headers = headers) 
    #print(r2.text)
    data2 = json.loads(r2.content)
    btr_amount = data2['btr_required_amount']
    btr_addr = data2['btr_receiving_address']
    btr_pid = data2['btr_required_payment_id']
    print("send ", str(btr_amount), " btr to", btr_addr, "with pid", btr_pid)        
    return uuid, btr_amount, btr_addr, btr_pid
    
    
    
#dest = "1em2WCg9QKxRxbo6S3xKF2K4UDvdu6hMc" #your dest address here
#amount = "0.1" #your amount here...

#uuid, btr_amount, btr_addr, btr_pid = btc2btr(dest, amount)
    
