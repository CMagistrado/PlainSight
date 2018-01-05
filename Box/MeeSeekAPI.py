#!/usr/bin/env python
from bitcoin import *
from multiprocessing import Process
from tqdm import tqdm
import json, time, boto3, requests, time, MySQLdb

class MeeSeek:

    def __init__(self):
        self.id = time.time()
        self.TTL = 1
        #self.MeekSeeNumber = MeekSeeNumber+1

# ------------------------------------------------------------------ #
#                           File Section
# ------------------------------------------------------------------ #

    def ofile(self, file):
        f = open(file, 'r')
        return


# ------------------------------------------------------------------ #
#                           SQS Section
# ------------------------------------------------------------------ #

    def sqsConnect(self):
        SQSclient = boto3.client('sqs')
        return SQSclient

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

    def sndMSG(self, content, url):
        client = self.sqsConnect()
        client.send_message(QueueUrl=url, MessageBody=content)
        return

    def delMSG(self, SQSclient, QUrl, responseMSG):
        goback = responseMSG['Messages'][0]
        receipt_handle = goback['ReceiptHandle']
        SQSclient.delete_message(QueueUrl=QUrl, ReceiptHandle=receipt_handle)
        print "I DELETED THE SQS MESSAGE!"
        return

# ------------------------------------------------------------------ #
#                           Insight API Section
# ------------------------------------------------------------------ #

    # Checks the current and unconfirmed balances.
    def unconfirmedB(self, addr):

        try:
            url = "http://ec2-34-236-37-17.compute-1.amazonaws.com:3001/insight-api/addr/" + addr + "/unconfirmedBalance"
            r = requests.get(url)
            pass

        except:
            print("Error with GET " + url)
            return 0
        
        # Balance check
        if (int(r.text)):
            return r.text

        return False
    
    def currentB(self, addr):

        try:
            url = "http://ec2-34-236-37-17.compute-1.amazonaws.com:3001/insight-api/addr/" + addr + "/balance"
            r = requests.get(url)
            pass
        
        except:
            print("Error with GET " + url)
            return 0

        if (int(r.text)):
            return r.text

        return False

    # Checks if money has been spent from address.
    def moneySpent(self, addr):

        try:
            url = "http://ec2-34-236-37-17.compute-1.amazonaws.com:3001/insight-api/addr/" + addr + "/totalSent"
            r = requests.get(url)

        except:
            print("Error with GET " + url)
            return 0

        if (int(r.text)):
            return r.text

        return False

    # Checks if money has been spent from address.
    def getTX(self, addr):

        try:
            # Get block with address in it
            blockURL = "http://ec2-34-236-37-17.compute-1.amazonaws.com:3001/insight-api/txs/?address=" + addr
            block = requests.get(blockURL)

        except:
            print("Error with GET: " + blockURL)
            return 0

        # Going to have to cut this json the fuck up
        # Parses to get the transaction time.
        parsed_json = json.loads(block.text)
        epoch_blocktime = parsed_json['txs'][0]['time']
        tx_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_blocktime))

        return tx_time

    return False

    def totalItems(self, addr):
        base = "http://ec2-34-236-37-17.compute-1.amazonaws.com:3001"
        url = base + "/insight-api/addrs/" + addr + "/txs?from=0&to=50"
        r = requests.get(url)
        parsed_json = json.loads(r.text)
        numItem = parsed_json["totalItems"]
        return numItem,parsed_json

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
#                           MarinaDB Database Section
# ------------------------------------------------------------------ #

    def mariaConnect(self):
        myDB = MySQLdb.connect(host="alladdresses.czebeja2ebtt.us-east-1.rds.amazonaws.com",port=3306,user="Rick",passwd="Memlab.0",db="AllAddresses")
        c = myDB.cursor()
        return

    def createTableTX(self, addr):
        # Working create table statement
        c.execute("CREATE TABLE " + addr + "(Timestamp INT NOT NULL, Friend VARCHAR(34) NOT NULL, Received TINYINT(1), Sent TINYINT(1), ValueIN INT, ValueOUT INT)")
        return

    def insertC(self, addr, priv, d, cAmount):
        c.execute("INSERT INTO Child")
        return

    # Gathers time of tx, address of sender to child, bool rcv, bool sent, ValueIN, ValueOUT, txid of sender txid for receiving
    def pushTX(self, parsedJSON, numItem):
        for number in numItem:
            time = parsedJSON["items"][number]["time"]         # Gets time of tx

            # Gets all the values and data per tx based on the addr
            # a) Get all number of items
            # aa) Get all "time" per item to sort chronologically.
            # b) get all vin and vout numbers per item
            # c) if (parsed_json["items"][0]["vin"][i]["addr"] == addr):
            #       vin/vout + itemNumber = parsed_json["items"][0]["vin"][i]["value"]
            #       determine if it's vin or vout
            #       item + time = parsed_json["items"][0]["vin"][i]["value"]
            #
            # Indiviual TX Logic
            #
            # Given: 
            #   0. First tx must be a receive
            #   1. TX is either send or receive
            #   2. TX can have 1 to multiple, multiple to 1, or 1 to 1.
            #
            #
            # Case A:
            # if (child sends aka vin):
            #   0. if (addr = parsedJSON["items"][item]["vin"][tx]["addr"])
            #   1.  value = parsedJSON["items"][item]["vin"][tx]["value"]   # get value from vout
            #   2.  txid = parsedJSON["items"][item]["txid"]                # get txid from item (this is the only info we can get as to where it was sent to)
            #   3.  write to db a send Table
            #
            # Case B:
            # if (child receives aka vout):
            #   0. if (addr == parsedJSON["items"][item]["vout"][tx]["scriptPubKey"]["addresses"]["addr"])
            #   1.  txid = parsedJSON["items"][item]["vin"][tx]["txid"] (tx == tx number of item number)
            #   2.  value = parsedJSON["items"][item]["vin"][tx]["value"]
            #   3.  senderAddr = parsedJSON["items"][item]["vin"][0]["addr"]
            #   4.  write to db a rev Table
            #
            # vin contains a TXID of the money being sent somewhere, so in the case of A,
            # get the txid of the vin of 

            # a) Get all number of items
            itemNum = len(parsedJSON["items"])

            # b) Iterates through all items
            for item in range(0,itemNum):

                # Gets number of vin and vout per item
                itemVinNum = len(parsedJSON["items"][item]["vin"])
                itemVoutNum = len(parsedJSON["items"][item]["vout"])

                # Gets all the Vin txs (Child Sends)
                for tx in range(0,itemVinNum):

                    if (addr == parsedJSON["items"][item]["vin"][tx]["addr"]):
                        typeofTX = "vout"
                        value = parsedJSON["items"][item]["vin"][tx]["value"]   # get value from vout
                        txid = parsedJSON["items"][item]["txid"]                # get txid from item (this is the only info we can get as to where it was sent to)
                        time = time.time()
                        self.insertTX(time, typeofTX, value, txid)


                # Gets all the Vout txs (Child Receives)
                for tx in range(0,itemVoutNum):

                    if (addr == parsedJSON["items"][item]["vout"][tx]["scriptPubKey"]["addresses"]["addr"])
                        typeofTX = "vin"
                        value = parsedJSON["items"][item]["vin"][tx]["value"]
                        txid = parsedJSON["items"][item]["vin"][tx]["txid"]
                        senderAddr = parsedJSON["items"][item]["vin"][0]["addr"]
                        time = time.time()
                        self.insertTX(time, typeofTX, value, txid, senderAddr)
                        
        return

    def insertTX(self, time, typeofTX, value, txid, senderAddr=False):

        # Logic to send tx. Stops at Child Receives 
        c.execute("CREATE TABLE " + addr + "(Timestamp INT NOT NULL, Friend VARCHAR(34) NOT NULL, Received TINYINT(1), Sent TINYINT(1), ValueIN INT, ValueOUT INT)")
        

        # This is in case it's a Child Receives funds
        if (senderAddr):

        return


# ------------------------------------------------------------------ #
#                           DynamoDB Database Section
# ------------------------------------------------------------------ #

    # Connect to Database
    def connectDB(self):
        print "Connecting to Database..."
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('BTC_Derive_Address')
        print("Connected!")
        return table

    # Check Database to see if d is already in it.
    def lookupDB(self, derive, table):
        print "Looking for derived of: %s" % derive
        responseDB = table.get_item(Key = {'d':derive})

        # If the item is in the database, return False
        # This might be broken....
        try:    
            item = responseDB['Item']['private_key']
            print("Item: %s" % item)
            return False
        
        # If the item is NOT the database, return True
        except:
            return True

    # Write to Database
    def pushDB(self, derive, priv, addr):
        DBclient = boto3.client('dynamodb')
        DBclient.put_item(TableName="BTC_Derive_Address", Item={'private_key':{'S':priv},'addr':{'S':addr},'d':{'S':derive}})
        print("I PUSHED A KEY!")
        return

    def validateD(self, derive):
        # Validates that the message is a derivative of type btc address
        if (len(derive) > 34) or (len(derive) < 26) or ("O" in derive) or ("I" in derive) or ("0" in derive) or ("l" in derive) or (" " in derive):
            print("This is not a Bitcoin Address.")
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