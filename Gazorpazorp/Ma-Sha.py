#!/usr/bin/env python
from multiprocessing import Process
import json, time, boto3, Gazorpazorp
"""
    1. Ensure Tor is up.
    2. Connect to SQS
    3. Get msg
    4. Parse message
    5. Connect to database
    6. Get addr from database
    7. Create transaction
    8. Send transacstion.
    9. Notify (Optional)

"""

def CreateGazorpazorp(xxx):

        #1. Create MeeSeek
        G = Gazorpazorp.Gazorpazorp()
        while (G.TTL):
            print "GAZORPAZORP!!!!"
            
            # 1. Connect to SQS
            # () ----> sqsMoneyCli
            # sqsMoneyCli[0] = SQSclient
            try:
                sqsMoneyCli = G.sqsConnect()

            except:
                print "Couldn't connecte to SQS"
                return 0    # Trigger a CloudWatch Event
            
            # 2. Check getMSG
            # (SQSMoneyclient, QUrl) --> (responseMSG, message)
            # rcvMSG[0]: "private_key:amount"
            # rcvMSG[1]: message. It is the derivative. In our case, the public address
            try:
                moneyQUrl = "https://sqs.us-east-1.amazonaws.com/508746504919/Cashmeoutside"
                rcvMSG = G.getMSG(sqsMoneyCli[0], moneyQUrl)
                
                if rcvMSG is False:
                    print "MY PURPOSE HAS BEEN SERVED!"
                    return 0
                pass

            except:
                print "Error with getting msg."
                return 0    # Trigger a CloudWatch Event

            # 2b. Parse mesage
            # rcvMSG[0]: "private_key:amount"
            # parse[0]: 'private_key'
            # parse[1]: 'amount'
            try:
                parse = G.parseMSG(rcvMSG[0])

            except:
                print "Parsing Error"
                return 0

            # 3. Validation Check, Delete Message
            #    (private_key) --> (T/F)
            #    Returns True if it's a public address
            if (G.validatePriv(parse[0]) is not True):
                G.delMSG(sqsMoneyCli[0], sqsMoneyCli[1], rcvMSG[0])
                print "This isn't a real private key!"  # Send Alert to CloudWatch w/ content
                return 0

            # 4. SQS addr Queue
            # -------------------------- #
            #   a. Connect to SQS
            #   b. Get msg
            # -------------------------- #
            # 4a. Connect to SQS
            # () ----> sqsMoneyCli
            # sqsCli[0] = SQSclient
            try:
                sqsBankCli = G.sqsConnect()

            # 5. Check getMSG
            # (SQSMoneyclient, QUrl) --> (responseMSG, message)
            # rcvMSG[0]: Used to go back and delete message once done.
            # rcvMSG[1]: public address that will be sent money
            try:
                bankQUrl = "https://sqs.us-east-1.amazonaws.com/508746504919/addr"
                rcvMSG = G.getMSG(sqsBankCli[0], bankQUrl)
                rcvMSG[1] = sendAddr
                
                if rcvMSG is False:
                    print "MY PURPOSE HAS BEEN SERVED!"
                    return 0
                pass

            except:
                print "Error with getting msg."
                return 0    # Trigger a CloudWatch Event


            # 6. Create transaction
            #  -------------------------- #
            #   electrum send.
            # --------------------------- #



            # 6. Delete Message and Die
            # (SQSclient, QUrl, responseMSG) --> return
            try:
                G.delMSG(sqsMoneyCli[0], sqsMoneyCli[1], rcvMSG[0])
                print "MY PURPOSE HAS BEEN SERVED!"
                pass

            except:
                print "Error Deleting MSG from SQS"
                pass    # Trigger a CloudWatch Event

            return 0

if __name__ == "__main__":

    while (tor):
        print "Tor Connected!"