# PlainSight

After the discovery of a paper online which describes how some bitcoin private keys are generated, we went on the treasure hunt to see if we could find addresses that had money still in them. We used AWS to build, and auto-deploy MeeSeeks, that would take any transaction that is added to the Bitcoin Blockchain, strip it for the BTC address, and use that address to generate a private key. We stopped after converting about 2 Million addresses, and concluded that whomever HAD been creating Bitcoin Addresses in this manner, is not currently using this poorly implemented method to derive private keys.

## Our Setup
* 1 m5.4xlarge EC2 Instance for BitCore
* 2 t2.xlarge EC2 Instances for MeeSeeks
* 3 Simple Queue Services for tx, spent, money queues
* 2 DynamoDB Servers

We had all the incoming txs send to AWS's Simple Queue Service, which allowed our MeeSeeks to grab an item (address) from the queue, lookup to see if it was already in our db. If so, die. Else, derive a key, and push that key to DynamoDB.

## Getting Started

Warning. MANY MeeSeeks died in the making of this, but all of them have lived a purposeful life.
Make changes to the parts where they interact with AWS, and make the, interact to yours

### Prerequisites
* BitCore
* boto3 for interact with AWS
* requests
* multiprocessing
* time
* json

```
python MeeSeekBox.py
```

### Installing

```
git clone https://github.com/CMagistrado/PlainSight.git
```


## Deployment

There have been a few bugs in MeeSeekBox that happens and dies from time to time.
Be sure not to use this in production without testing this, or setting up an alert if it crashes.

## Authors

* **Chris Magistrado**
