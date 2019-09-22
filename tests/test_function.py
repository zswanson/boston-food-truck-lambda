import sys, os
import pytest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import function

fields = ['Truck', 'Location', 'Pinpoint', 'Link']

valid_locations = [
    'Stuart Street',
    'Boston Public Library'
]

week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

invalid_location = 'Not A Real Location'


def test_is_weekend():
    assert function.is_weekend('Monday') is False
    assert function.is_weekend('Saturday') is True


def test_valid_locations():
    for loc in valid_locations:
        for day in week:
            r = function.get_food_trucks(loc, day)
            for item in r:
                for field in fields:
                    assert field in item.keys()
                assert item['Location'] == loc


def test_invalid_locations():
    r = function.get_food_trucks(invalid_location, 'Monday')
    assert r == []


def test_env_locations_missing():
    with pytest.raises(KeyError):
        x = function.get_env_locations()


def test_get_dinner_schedule():
    loc = 'Maverick Square'
    day = 'Monday'
    response = function.get_food_trucks(loc, day, 'Dinner')
    print(response)
    assert response is not None and response != []
    assert len(response) >= 1
