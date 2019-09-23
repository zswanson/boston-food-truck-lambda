Slack 'bot' that runs as an AWS lambda so that it can be scheduled.
Queries the Boston Food Truck ArcGIS API to get trucks at specified locations, then posts to a Slack webhook endpoint.
Ignores weekend days and for now will only report the Lunch schedule.

![Sample output from slack channel](https://raw.githubusercontent.com/zswanson/boston-food-truck-lambda/master/images/sample.png "Sample Slack Output")

Must provide the following environment variables:
* `SLACK_TOKEN`: the app/webhook token generated from Slack
* `LOCATIONS`: A comma separated list of food truck locations to report on. The values must precisely match this set:
    * Boston Public Library
    * Clarendon Street
    * Stuart Street
    * Belvidere Street
    * Charlestown Navy Yard
    * Ashmont Station
    * Milk and Kirby Streets
    * Pearl and Franklin Streets
    * Maverick Square
    * 77 Avenue Louis Pasteur
    * BU East
    * BU West
    * Opera Place
    * Dudley Square
    * Boston Medical Center
    * Peter's Park
    * Seaport District
    * Blossom Street at Emerson Place
    * Hurley Building
    * there's a few others; I need to check their syntax

Depends on: requests, pytest (testing only)

Usage:

Add the function package to AWS Lambda and set a CloudWatch schedule trigger. Provide the environment variables noted above. No IAM privileges are required. There are several different ways to setup the Slack side of this, so that's up to you. I suggest having it send to a private channel first to test it out.
