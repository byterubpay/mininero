import MiniNero
import ed25519
import binascii
import PaperWallet
import cherrypy
import os
import time
import bitbyterubd
import SimpleBTR2


btr_addr = "44TVPcCSHebEQp4LnapPkhb2pondb2Ed7GJJLc6TkKwtSyumUnQ6QzkCCkojZycH2MRfLcujCM7QR1gdnRULRraV4UpB5n4"
btr_amount = "0.25"
btr_pid = "d8dd8f42cb13f26dbbf86d2d1da061628cdd17781be95e58a21c845465a2c7f6"

bitbyterubd.send(btr_addr, float(btr_amount), btr_pid, 3) 

