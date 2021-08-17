from json import dumps, loads
import random
from uuid import uuid4

import pytest
import requests
from assertpy.assertpy import assert_that, soft_assertions
from jsonpath_ng import parse

from config import BASE_URI
from tests.utils.people_utils import create_person_with_unique_last_name, search_created_user_in
from utils.file_reader import read_file


def test_read_all_has_kent():
    # given - when
    # We use requests.get() with url to make a get request
    response = requests.get(BASE_URI)
    # response from requests has many useful properties
    # we can assert on the response status code
    # then
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    # We can get python dict as response by using .json() method
    response_text = response.json()
    first_names = [people['fname'] for people in response_text]
    assert_that(first_names).contains('Kent')


def test_new_person_can_be_added():
    # given - when
    unique_last_name = create_new_person()

    # then
    # After user is created, we read all the users and then use filter expression to find if the
    # created user is present in the response list
    peoples = requests.get(BASE_URI).json()
    is_new_user_created = search_created_user_in(peoples, unique_last_name)
    assert_that(is_new_user_created).is_not_empty()


def test_read_all_has_kent_soft_assertion():
    # given - when
    # We use requests.get() with url to make a get request
    response = requests.get(BASE_URI)
    # response from requests has many useful properties
    # we can assert on the response status code
    # then
    with soft_assertions():
        assert_that(response.status_code).is_equal_to("any wrong code")
        # We can get python dict as response by using .json() method
        response_text = response.json()
        first_names = [people['fname'] for people in response_text]
        assert_that(first_names).contains('Kent')


def test_created_person_can_be_deleted():
    # given
    persons_last_name = create_new_person()
    peoples = requests.get(BASE_URI).json()
    newly_created_user = search_created_user_in(peoples, persons_last_name)[0]
    delete_url = f'{BASE_URI}/{newly_created_user["person_id"]}'

    # when
    response = requests.delete(delete_url)

    # then
    assert_that(response.status_code).is_equal_to(requests.codes.ok)


def create_new_person() -> str:
    # Ensure a user with a unique last name is created everytime the test runs
    # Note: json.dumps() is used to convert python dict to json string
    unique_last_name = f'User {str(uuid4())}'
    payload = dumps({
        'fname': 'New',
        'lname': unique_last_name
    })

    # Setting default headers to show that the client accepts json
    # And will send json in the headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # We use requests.post method with keyword params to make the request more readable
    response = requests.post(url=BASE_URI, data=payload, headers=headers)
    response.headers
    assert_that(response.status_code, description='Person not created').is_equal_to(requests.codes.no_content)
    return unique_last_name


@pytest.fixture
def create_data():
    payload = read_file('create_person.json')

    random_no = random.randint(0, 1000)
    last_name = f'Olabini{random_no}'

    payload['lname'] = last_name
    yield payload


def test_person_can_be_added_with_a_json_template(create_data):
    create_person_with_unique_last_name(create_data)

    response = requests.get(BASE_URI)
    peoples = loads(response.text)

    # Get all last names for any object in the root array
    # Here $ = root, [*] represents any element in the array
    # Read full syntax: https://pypi.org/project/jsonpath-ng/
    jsonpath_expr = parse("$.[*].lname")
    result = [match.value for match in jsonpath_expr.find(peoples)]

    expected_last_name = create_data['lname']
    assert_that(result).contains(expected_last_name)

