import os
sec = raw_input("wallet pass?")
os.system(" ~/bitbyterub/build/release/bin/simplewallet --wallet-file ~/wallet/testwallet1 --password "+sec+" --rpc-bind-port 18082")
