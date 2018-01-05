#!/usr/bin/env python
import time, MeeSeekAPI, requests, multiprocessing
from multiprocessing import Pool
from tqdm import tqdm

# Resources
# http://www.blopig.com/blog/2016/08/processing-large-files-using-python/
# 65k tx 1N52wHoVR79PMDishab2XmRHsbekCdGquK
# 4 tx 1KPMheWsbN7VmpX895rDeDpfbZtmsygZjD
# 0 tx 36pr77wB2sEJCFEhqeY1DTzkiNRmBVVg2h


def CreateMeeSeek(line):

        #1. Create MeeSeek
        M = MeeSeekAPI.MeeSeek()

        while (M.TTL):
            print("I'M MR. MEESEEKS! LOOK AT ME!!")

            # 1. Validate
            # 2. genMoney
            # 2b validate
            # 3. Check balance of addr
            # 4. Check unconfirmed and received amounts
            # 5. If any of those:
            #       API call to get info
            # 5b Create TX Table
            # 6. Get TX Data
            # 7. Store information into appropriate table in db

            # 1. Validation Check, Delete Message
            #    (derive) --> (T/F)
            #    Returns True if it's a public address
            if (M.validateD(line) is not True):
                return 0

            # 2. genMoney
            # (derive) --> derive,priv,addr
            # result[0]: derive
            # result[1]: priv
            # result[2]: addr
            try:
                result = M.genMoney(line)
                pass

            except:
                print("Error generating keys")
                return 0    # Trigger a CloudWatch Event

            # Setup variables for later use
            d = result[0]
            priv = result[1]
            cAddr = result[2]

            # 3. If there's any TXs, then activity exists.
            # If true, activity exists
            # txData[0] = Number of TXs
            # txData[1] = r.text as parsed json
            try:
                txData = M.totalItems(cAddr)
                pass

            except:
                print("Could not get TX Data.")
                return 0 

            if (M.totalTX(cAddr)):
                continue

            else:
                return 0

            # 4. MariaDB
            # -------------------------------------------------- #
            #   a. Connect to Database
            #   b. Push to Children Table
            #   c. Create TX Table and INSERT to each table
            # -------------------------------------------------- #                
            try:
                M.mariaConnect()
                pass
            
            except:
                print("Error pushing to MariaDB")
                return 0

            # INSERT data into Child Table
            # result[0]: derive
            # result[1]: priv
            # result[2]: cAddr
            priv = result

            try:
                M.insertC(cAddr, priv, d, cAmount)
                pass
            
            except:
                print("Error INSERT into table Children")
                return 0


            # Gather currentBalance, unconfirmedBalance, and moneySpent
            currentB = M.currentB()
            unconfirmedB = M.unconfirmedB()
            moneySpent = M.moneySpent()

            # 5. Parse, Create TX Table, and INSERT data to table

            # a) Parse all data accordingly
            try:
                M.pushTX(txData[1], txData[0])
                pass

            except:
                print("Could not parsed TX Data.")
                return 0

            # Receives all the data that will be put into TX Table
            try:
                M.txGET(cAddr)
                pass
            
            except:
                print("Couldn't get TX Data")
                return 0

            # CREATE a Table for the all the transactions an address has
            try:
                M.createTableTX(cAddr)
                pass
            
            except:
                print("Could not create table in MariaDB")
                return 0

            # INSERTS all the data into the TX Tables
            try:
                M.insertTX()
                pass
            
            except:
                print("Couldn't INSERT data into MariaDB")
                return 0
        
        return 0

# ------------------------------------------------------------------------------------------------ #

def process(line):
    CreateMeeSeek(line)
    return

def process_wrapper(lineByte):
    with open("10.txt") as f:
        f.seek(lineByte)
        line = f.readline()
        process(line)
        return

if __name__ == "__main__":


    # 0. init objects
    t0=time.time()
    cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(cores)
    jobs = []
    #result = pool.map(CreateMeeSeek,range(10))  
    
    # 1. Connect to Database
    try:
        M.mariaConnect()

    except:
        print "Couldn't connect to MariaDB"
        return 0    # Trigger a CloudWatch Event
            

    # 2. Open address file
    #create jobs
    with open("10.txt") as f:
        nextLineByte = f.tell()
        for line in f:
            jobs.append( pool.apply_async(process_wrapper,(nextLineByte)) )
            nextLineByte = f.tell()

    # 3. wait for all jobs to finish
    for job in jobs:
        job.get()

    #clean up
    pool.close()
    t1=time.time()
    print("Time Elapsed: %s" % str(t1-t0))
