# Openchat
[![CircleCI](https://circleci.com/gh/jvalduvieco/openchat/tree/master.svg?style=svg)](https://circleci.com/gh/jvalduvieco/openchat/tree/master)
[![codecov](https://codecov.io/gh/jvalduvieco/openchat/branch/master/graph/badge.svg)](https://codecov.io/gh/jvalduvieco/openchat)

This is an implementation of the [openchat](https://github.com/sandromancuso/cleancoders_openchat) project by [unclebob](https://twitter.com/unclebobmartin) and
[Sandro Mancuso](https://twitter.com/sandromancuso) in their [Comparative case study videos](https://cleancoders.com/videos/comparativeDesign), highly recommended BTW.

This implementation is a deliverate practice made in Python as I need to learn the language also used some kind of clean / CQRS architecture to continue learning.

## Rationale
These are the principles I've tried to follow:
* Be efficient. Write the less infrastructure code as possible
* Be familiar. Don't drink too much functional/CQRS/Clean brew
* Be expressive. Allow non technical readers read business code.
* Make code movable
* Make little assumptions about future (were this code will run, what will grow, ...)
* Allow grow 
* YAGNI
* Irritate the reader and the writer


## What should you expect from current code
A set of tests that run without errors implementing all domain included in API.md and one endpointexposed at HTTP REST API level.
* Happy paths
* Minimum error handling
* No database
* Some inconsistencies
  - Do I want a Query bus? 
  - Should queries have a query DTO?
* Some code that should not be there and some repetition (esp. in tests)
* Not very ugly things. Just WIP.

Feature complete


## Installing
* Clone the repo
* [Install Pipenv](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv)
* Install deps:
```
pipenv install --dev
```
* Run tests
```
pipenv run tests
```
* Run a development server
```
pipenv run start_restapi_dev
```
