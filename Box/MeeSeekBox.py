#!/usr/bin/env python
from multiprocessing import Pool
import time, MeeSeek, multiprocessing

"""
1. Create MeekSeekQueue
2. Create MeekSeek
3
# ------------------------------------------------------------------------- #
# 1. Get id, tell MeeSeekQueue
# ------------------------------------------------------------------------- #

   pool = Pool(10,maxtasksperchild=1)
    results = pool.imap_unordered(function, params)
    for r in results:
        # do things with "r"
    pool.close()
    pool.join()

    pool_size = multiprocessing.cpu_count() * 2
    pool = multiprocessing.Pool(processes=pool_size,
        initializer=start_process,
        maxtasksperchild=2,
        )
    pool_outputs = pool.map(do_calculation, inputs)


    while MeeSeekQ.empty() is True:
        # Message EC2 to sent SNS

def f(n):
    sum = 0
    for x in range(1000):
        sum += x*x
    return n
"""

def CreateMeeSeek(xxx):

        #1. Create MeeSeek
        M = MeeSeek.MeeSeek()
        while (M.TTL):
            print "I'M MR. MEESEEKS! LOOK AT ME!!"
            
            # 1. Connect to SQS
            # sqsCli[0] = SQSclient
            # sqsCli[1] = QUrl
            try:
                sqsCli = M.sqsConnect()

            except:
                print "Couldn't connecte to SQS"
                return 0    # Trigger a CloudWatch Event
            
            # 2. Check getMSG
            # (SQSclient, QUrl) --> (responseMSG, message)
            # rcvMSG[0]: responseMSG. This is used as a handler to delete the message
            # rcvMSG[1]: message. It is the derivative. In our case, the public address
            try:
                rcvMSG = M.getMSG(sqsCli[0], sqsCli[1])
                
                if rcvMSG is False:
                    print "MY PURPOSE HAS BEEN SERVED!"
                    return 0
                pass

            except:
                print "Error with getting msg."
                return 0    # Trigger a CloudWatch Event

            # 3. Validation Check, Delete Message
            #    (derive) --> (T/F)
            #    Returns True if it's a public address
            if (M.validateD(rcvMSG[1]) is not True):
                M.delMSG(sqsCli[0], sqsCli[1], rcvMSG[0])
                print "MY PURPOSE HAS BEEN SERVED!"
                return 0

            # 4. Database
            # -------------------------- #
            #   a. Connect to Database
            #   b. Lookup Database
            #   c. GenMoney
            #   d. Push
            # -------------------------- #
            # 4a. Connect to Database
            # () --> table
            try:
                table = M.connectDB()

            except:
                print "Error connecting to Database"
                return 0    # Trigger a CloudWatch Event

            # 4b. Lookup Database
            # (derive, table) --> (T/F)
            if (M.lookupDB(rcvMSG[1], table)) is not True:
                M.delMSG(sqsCli[0], sqsCli[1], rcvMSG[0])
                print "MY PURPOSE HAS BEEN SERVED!"
                return 0

            # 4c. genMoney
            # (derive) --> derive,priv,addr
            # result[0]: derive
            # result[1]: priv
            # result[2]: addr
            try:
                result = M.genMoney(rcvMSG[1])

            except:
                print "Error generating keys"
                return 0    # Trigger a CloudWatch Event


            # 4d. (derive, priv, addr) --> return
            try:
                M.pushDB(rcvMSG[1], result[1], result[2])
            
            except:
                print "Error writing to DB" # Trigger a CloudWatch Event
                return 0

            # 5. Delete Message and Die
            # (SQSclient, QUrl, responseMSG) --> return
            try:
                M.delMSG(sqsCli[0], sqsCli[1], rcvMSG[0])
                print "MY PURPOSE HAS BEEN SERVED!"
                pass

            except:
                print "Error Deleting MSG from SQS"
                pass    # Trigger a CloudWatch Event

            return 0


if __name__ == "__main__":

    while(1):
        result=[]
        
        t1=time.time()
        pool_size = multiprocessing.cpu_count() * 2
        pool = Pool(processes=pool_size)
        result = pool.map(CreateMeeSeek,range(10))
        pool.close()
        pool.join()

        t2=time.time()
        result.append(t2-t1)

        print result
"""
if __name__ == "__main__":

    result=[]

    for i in range(1):
        t1 = time.time()
        CreateMeeSeek()
        t2 = time.time()
        result.append(t2-t1)
    
    print result
"""