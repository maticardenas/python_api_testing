from json import dumps
from typing import Dict, Any, Optional, List
from uuid import uuid4

import requests
from assertpy import assert_that

from config import BASE_URI
from utils.json_utils import get_prop_from_str_payload


def create_person_with_unique_last_name(body: Optional[Dict[str, str]] = None) -> str:
    payload = _get_person_payload(body)
    unique_last_name = get_prop_from_str_payload(payload, "lname")
    # Setting default headers to show that the client accepts json
    # And will send json in the headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # We use requests.post method with keyword params to make the request more readable
    response = requests.post(url=BASE_URI, data=payload, headers=headers)
    assert_that(response.status_code, description='Person not created').is_equal_to(requests.codes.no_content)
    return unique_last_name


def _get_person_payload(body: Dict[str, Any]) -> Dict[str, Any]:
    if not body:
        # Ensure a user with a unique last name is created everytime the test runs
        # Note: json.dumps() is used to convert python dict to json string
        unique_last_name = f'User {str(uuid4())}'
        payload = dumps({
            'fname': 'New',
            'lname': unique_last_name
        })
    else:
        payload = dumps(body)

    return payload


def search_created_user_in(peoples: Dict[str, str], last_name: str) -> List[Dict[str, str]]:
    return [person for person in peoples if person['lname'] == last_name]