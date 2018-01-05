#!/usr/bin/python env
import MeeSeekAPI, time
from multiprocessing import Process
from multiprocessing import Pool
import time, MeeSeekAPI, multiprocessing, requests

def MeeFile(xxx):
    #MeeFile.py
    f = open('gen_addr', 'r')

    M = MeeSeekAPI.MeeSeek()
    pk = "NULL"

    balance = "https://sqs.us-east-1.amazonaws.com/508746504919/balance_children"
    spent = "https://sqs.us-east-1.amazonaws.com/508746504919/children_spent"

    for line in f:
        M.addrBalance(line, balance, pk)
        M.moneySpent(line, spent)

if __name__ == "__main__":

    result=[]

    while(1):
        t1=time.time()
        pool_size = multiprocessing.cpu_count() * 2
        pool = Pool(processes=pool_size)
        result = pool.map(MeeFile,range(10))
        pool.close()
        pool.join()

        t2=time.time()
        result.append(t2-t1)

    print result