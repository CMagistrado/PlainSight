# PlainSight

After the discovery of a paper online which describes how some bitcoin private keys are generated, we went on the treasure hunt to see if we could find addresses that had money still in them. We used AWS to build, and auto-deploy MeeSeeks, that would take any transaction that is added to the Bitcoin Blockchain, strip it for the BTC address, and use that address to generate a private key. We stopped after converting about 2 Million addresses, and concluded that whomever HAD been creating Bitcoin Addresses in this manner, is not currently using this poorly implemented method to derive private keys.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

boto3 for interact with AWS
requests
multiprocessing
time
json

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

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Chris Magistrado**
