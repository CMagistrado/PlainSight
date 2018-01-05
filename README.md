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

### Prerequisites
* BitCore
* boto3 for interact with AWS
* requests
* multiprocessing
* time
* json

```
Give examples
```

### Installing

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Authors

* **Chris Magistrado**
