import MiniNero
import ed25519
import binascii
import PaperWallet
import cherrypy
import os
import time
import bitbyterubd
import SimpleBTR2

lasttime = 0

def HexSigningPubKey(s):
  return binascii.hexlify(ed25519.publickey(ed25519.encodeint(MiniNero.hexToInt(s))))

def Signature(m, sk):
  #note this seems to return nicely sized version of the signature
  #contrast with, i.e. tweetnacl..
  sk2 = ed25519.encodeint(MiniNero.hexToInt(sk))
  pk = ed25519.publickey(sk2)
  return binascii.hexlify(ed25519.signature(m, sk2, pk))

def Verify(sig, m, pk):
  return ed25519.checkvalid(binascii.unhexlify(sig), m, binascii.unhexlify(pk))

class MiniNeroServer:

    exposed = True

    def GET(self, id=None):
        times = str(int(time.time()))
        return (times)

    def POST(self, signature, Type, timestamp, amount=None, destination=None, pid=None, mixin=None):
        times= int(time.time())
        pubkey = MiniNeroPk
        global lasttime
        if (abs(times - int(timestamp)) > 30):
            ver = False
            return ('fail based on timestamp too old')
        else:
          if Type == 'address':
              message = Type+timestamp
              ver = Verify(signature.encode("utf8"), message.encode("utf8"), pubkey)
              if (ver):
                  print("getting address")
                  address = bitbyterubd.myAddress()
                  return (str(address))
          if Type == 'balance':
              message = Type+timestamp
              ver = Verify(signature.encode("utf8"), message.encode("utf8"), pubkey)
              if (ver):
                  print("getting balance")
                  balance = bitbyterubd.balance()
                  return (str(float(balance)/1000000000000))
          if Type == 'send':
              message = Type+amount.replace('.', 'd')+timestamp+destination
              ver = Verify(signature.encode("utf8"), message.encode("utf8"), pubkey)
              if (ver) and (abs(times - lasttime >30 )):
                  #create btr2 order async, return uuid
                  uuid, btr_amount, btr_addr, btr_pid = SimpleBTR2.btc2btr(destination, amount)
                  bitbyterubd.send(btr_addr, float(btr_amount), btr_pid, 3) 
                  lasttime = times
                  return ('order uuid: '+uuid)
          if Type == 'sendBTR':
              message = Type+amount.replace('.', 'd')+timestamp+destination
              ver = Verify(signature.encode("utf8"), message.encode("utf8"), pubkey)
              if (ver) and (abs(times - lasttime >30 )):
                  #create btr2 order async, return uuid
                  #uuid, btr_amount, btr_addr, btr_pid = SimpleBTR2.btc2btr(destination, amount)
                  lasttime = times
                  btr_amount = amount
                  btr_addr = destination
                  btr_pid = pid
                  bitbyterubd.send(btr_addr, float(btr_amount), btr_pid, 3) 
                  return ('sent')
 
        

if __name__ == '__main__':

    #check if api pubkey is created, if not create it:
    if(os.path.isfile('MiniNeroPubKey.py')):
        from MiniNeroPubKey import *
    try:
        MiniNeroPk
    except NameError:
        MiniNeroSk= PaperWallet.skGen()
        MiniNeroPk= HexSigningPubKey(MiniNeroSk)
        print("Your new api secret key is:")
        print(MiniNeroSk)
        print("You should save this in a password manager")
        print("Your pubkey will be stored in MiniNeroPubKey.py")
        f = open('MiniNeroPubKey.py', 'w')
        f.write("MiniNeroPk = \'"+MiniNeroPk+"\'")
    print("Your MiniNeroServer PubKey is:")
    print(MiniNeroPk)
    lasttime = 0


    #Launch Cherry Server
    cherrypy.tree.mount(
        MiniNeroServer(), '/api/mininero',
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
        }
    )

    cherrypy.server.socket_host = '0.0.0.0' #run on metal
    cherrypy.engine.start()
    cherrypy.engine.block()
