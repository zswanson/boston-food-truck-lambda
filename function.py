from datetime import date
from ast import literal_eval
import calendar
import requests
import os
import foodmoji

# TODO: randomized leader messages
slackLeaderMessage = 'Hey! Are you staring at a boring :sandwich: for lunch? Try these trucks instead! :chompy:\n'
slackUrl = f'https://hooks.slack.com/services/'
slackBotName = 'FoodTruckBot'
slackBotEmoji = ':truck:'
bostonArcGisAccount = 'sFnw0xNflSi8J0uh'
queryUrl = f'https://services.arcgis.com/{bostonArcGisAccount}/arcgis/rest/services/food_truck_schedule/FeatureServer/0/query'
queryFields = 'Truck,Location,Pinpoint,Link'


def get_food_trucks(location: str, day: str, time: str = 'Lunch'):
    """
    get_food_trucks
    :param time: enumeration of Lunch or Dinner
    :param location: Specifc location that matches the exact text from the Boston food truck schedule
    :param day: long form day of the week - Monday, Tuesday etc
    :return: List of dictionaries with keys: Truck, Location, Pinpoint, Link
    :rtype list
    """

    payload = {
        'returnGeometry': 'false',
        'f': 'json',
        'where': f"Day='{day}' AND Time='{time}' AND Location='{location}'",
        'outFields': queryFields,
    }

    response = requests.get(queryUrl, payload)
    if response.status_code != 200:
        raise RuntimeError(f'ERROR: {queryUrl} returned invalid response: {response.status_code} \n{response.text}')
    if 'features' not in response.json().keys():
        raise ValueError(f'ERROR: Unexpected content in response:\n {response.text}')

    return [x['attributes'] for x in response.json()['features']]


def build_message(day: str, locations, time: str = 'Lunch'):
    """
    Primary business logic occurs here, makes the queries and builds the slack output message
    :param day: day of the weeek, full word
    :param time: Lunch or Dinner
    :return: formatted slack message
    :rtype str
    """
    message = ""
    for loc in locations:
        food_trucks = get_food_trucks(loc, day, time)
        if food_trucks != []:
            # pinpoint location is the same for each element, only check once
            pinpoint = food_trucks[0]['Pinpoint']
            # location header, using bold markdown
            message = message + f"*{loc} - {pinpoint}*\n"
            for truck in food_trucks:
                # some of the trucks have extra whitespace in the geojson
                name = str.rstrip(truck['Truck'])
                link = f"- {truck['Link']}" if truck['Link'] is not None else ''
                flair = foodmoji.get_foodmoji(name)

                # truck attributes are indented relative to the location, led by a bullet
                message = message + f"\t* {flair} {truck['Truck']} {link}\n"

    if message != "":
        return slackLeaderMessage + message
    else:
        return None


def is_weekend(day:str):
    return day in ['Saturday', 'Sunday']


def post_slack(message, token):
    payload = dict(username=slackBotName,
                   icon_emoji=slackBotEmoji,
                   text=message)
    response = requests.post(f"{slackUrl}{token}", json=payload)
    if response.status_code != 200:
        raise Exception(f'POST to Slack returned {response.status_code}, the response is:\n{response.text}')


def get_env_locations():
    try:
        return [x for x in os.environ['LOCATIONS'].split(',')]
    except KeyError:
        raise KeyError("ERROR: environment variable LOCATIONS not provided")
    except ValueError:
        raise ValueError("ERROR: LOCATIONS environment variable has an invalid format; "
                         "expected a string with comma separated values")


def get_env_token():
    try:
        return os.environ['SLACK_TOKEN']
    except KeyError:
        raise Exception("ERROR: environment variable SLACK_TOKEN not provided")


# TODO: logic to handle Lunch or Dinner based on time of day in the context, and an environment var
def lambda_handler(event, context):
    print(f"BostonFoodTruck Slackbot - version:{context.function_version}")

    if event and event['test'] == True:
        slack_token = event['token']
        locations = [x for x in event['locations'].split(',')]
        today = event['day']
    else:
        slack_token = get_env_token()
        locations = get_env_locations()
        today = calendar.day_name[date.today().weekday()]

    if is_weekend(today):
        print(f'{today} is a weekend, skipping')
        exit(0)

    slack_message = build_message(today, locations)
    if slack_message:
        print(f"Message as built: \n{slack_message}")
        post_slack(slack_message, slack_token)
    else:
        post_slack("Sorry guys, no food trucks found today! Hope you brought lunch. :( ", slack_token)


def main():
    print("BostonFoodTruck Slackbot - Testing - no Slack POST")
    today = calendar.day_name[date.today().weekday()]
    locations = ['Stuart Street', 'Boston Public Library', 'Clarendon Street']
    slack_message = build_message(today, locations)
    if slack_message:
        print(f"Message as built: \n{slack_message}")
    else:
        print(f"No food trucks found at {locations}? on {today}?")


if __name__ == "__main__":
    main()
