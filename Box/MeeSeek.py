#!/usr/bin/env python
from bitcoin import *
from multiprocessing import Process
import json, time, boto3

class MeeSeek:

    def __init__(self):
        self.id = time.time()
        self.TTL = 1
        #self.MeekSeeNumber = MeekSeeNumber+1

# ------------------------------------------------------------------ #
#                           SQS Section
# ------------------------------------------------------------------ #

    def sqsConnect(self):
        SQSclient = boto3.client('sqs')
        QUrl = "https://sqs.us-east-1.amazonaws.com/508746504919/tx"
        return SQSclient, QUrl

    def getMSG(self, client, QUrl):        
        # Receive/Check Queue
        try:
            responseMSG = client.receive_message(QueueUrl=QUrl)
            pass

        except:
            print "Couldn't connected to SQS Server"
            return -1

        try:
            message = responseMSG['Messages'][0]['Body']   # returns message
            print "I GOT SOMETHING!"
            pass

        except KeyError, e:
            # Create a post to CloudWatch saying KeyError
            # if n.workers > 0, decriment TTL = 1
            e = str(e)
            e = e.replace("'", "")
            if (e == 'Messages'):
                print "No msgs in queue."   # Trigger EC2 instance to trigger an SNS
                return False
            else:
                 # Trigger EC2 instance to trigger an SNS
                print "fix it"
            return False
        
        except:
            # Create a post to CloudWatch saying Non-KeyError issue
             # Trigger EC2 instance to trigger an SNS
            return False

        # YOUR ARE CHECKING TO SEE IF MSG IS DELETED AFTER THIS PROCESS
        return responseMSG, message

    def delMSG(self, SQSclient, QUrl, responseMSG):
        goback = responseMSG['Messages'][0]
        receipt_handle = goback['ReceiptHandle']
        SQSclient.delete_message(QueueUrl=QUrl, ReceiptHandle=receipt_handle)
        print "I DELETED THE SQS MESSAGE!"
        return

# ------------------------------------------------------------------ #
#                           Generate Keys Section
# ------------------------------------------------------------------ #

    # Generate Address
    def genMoney(self, derive):
        priv = sha256(derive) # Change this to change the derivative
        pub = privtopub(priv)
        addr = pubtoaddr(pub)
        return derive,priv,addr

# ------------------------------------------------------------------ #
#                           Database Section
# ------------------------------------------------------------------ #

    # Connect to Database
    def connectDB(self):
        print "Connecting to Database..."
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('BTC_Derive_Address')
        print "Connected!"
        return table

    # Check Database to see if d is already in it.
    def lookupDB(self, derive, table):
        print "Looking for derived of: %s" % derive
        responseDB = table.get_item(Key = {'d':derive})

        # If the item is in the database, return False
        # This might be broken....
        try:    
            item = responseDB['Item']['private_key']
            print "Item: %s" % item
            print "====================================================="
            print "MY PURPOSE ENDS HERE!"
            return False
        
        # If the item is NOT the database, return True
        except:
            print "++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            print "MY PURPOSE IS TO PUSH IT TO THE DATABASE!"
            return True

    # Write to Database
    def pushDB(self, derive, priv, addr):
        DBclient = boto3.client('dynamodb')
        DBclient.put_item(TableName="BTC_Derive_Address", Item={'private_key':{'S':priv},'addr':{'S':addr},'d':{'S':derive}})
        print "I PUSHED A KEY!"
        return

    def validateD(self, derive):
        # Validates that the message is a derivative of type btc address
        if (len(derive) > 34) or (len(derive) < 26) or ("O" in derive) or ("I" in derive) or ("0" in derive) or ("l" in derive) or (" " in derive):
            print "This is not a Bitcoin Address."
            return False
        return True

# ------------------------------------------------------------------ #
#                           Misc. Section
# ------------------------------------------------------------------ #
""" # Removing this because each MeeSeek will only run through this once, then die.
    def sleep(self):
        print "I'ma sleep."
        time.sleep(1)
        self.TTL = self.TTL - 1
        return
"""