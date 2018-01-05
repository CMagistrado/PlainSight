#!/usr/bin/python env
import MeeSeekAPI

#MeeFile.py
f = open('gen_addr', 'r')

M = MeeSeekAPI.MeeSeek()
pk = "NULL"

balance = "https://sqs.us-east-1.amazonaws.com/508746504919/balance_children"
spent = "https://sqs.us-east-1.amazonaws.com/508746504919/children_spent"

for line in f:
    M.addrBalance(line, balance, pk)
    M.moneySpent(line, spent)
