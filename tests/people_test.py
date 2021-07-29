from json import dumps
from typing import Dict, List
from uuid import uuid4

import requests
from assertpy.assertpy import assert_that, soft_assertions

from config import BASE_URI


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


def search_created_user_in(peoples: Dict[str, str], last_name: str) -> List[Dict[str, str]]:
    return [person for person in peoples if person['lname'] == last_name]
