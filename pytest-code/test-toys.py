import requests
import json
import sys

global id1,id2, toy1, toy2

toy1 = {
    "name": "blocks",
    "descr": "12 building blocks",
    "age": 3,
    "price": 18.00
}

toy2 = {
    "name": "puzzle",
    "descr": "30 piece puzzle",
    "age": 4,
    "price": 25.00
}


urlToys = 'http://localhost:8001/toys'

def assert_fields_equal(record1: dict, record2: any):
    if type(record2) != type(record1):  # check that record2 is also a dictionary
        # print(f'assert_fields_equal: Returned object is not of type {str(type(record1))}\n')
        return False
    for field in record1.keys():
        if field not in record2:
            # print(f'assert_fields_equal: Expected field named "{field}" in returned object but it was missing. Returned object = {record2}\n')x
            return False
        if record1[field] != record2[field]:
            # print(f'assert_fields_equal: Field "{field}" in returned object: {record2[field]} does not match expected value: {record1[field]}')
            return False
    # print("passed assert_fields_equal")
    return True


# test_collection_contains_field_values checks that given a list of objects, a json field name field, and a list of
# values, for each v in the list of values there exists a record r in coll such that r[field] = v
def assert_collection_contains_field_values(coll: list, field: str, values: list):
    # print(f"assert_collection_container_field_values:  coll = {coll}\n field = {field}\n values = {values}")
    for v in values:
        try:
            if not [c for c in coll if c[field] == v]:
                # print(f"assert_collection_contains_field_values: No object in returned array with {field} == {v}")
                return False
        except Exception as e:
            # print("failed assert_collection_contains_field_values")
            # print("Exception = ", str(e))
            return False
    # otherwise found that the collection satisfies the assertion
    return True


def test_post_toy1():
    global toy1, id1
    json_data = json.dumps(toy1)
    response = requests.post(urlToys,
        headers={"Content-Type":"application/json"},
        data=json_data)
    # print("response from POST toy1 is ", response.json())
    id1 = response.json()['id']
    assert response.status_code == 201


def test_get_toy1():
    global id1
    response2 = requests.get(urlToys + '/' + id1)
    # print(f"response from GET toys {id1} is {response2.json()}")
    assert response2.status_code == 200
    assert_fields_equal(toy1, response2.json())


def test_post_toy2():
    global toy2, id2
    json_data = json.dumps(toy2)
    response3 = requests.post(urlToys,
        headers={"Content-Type":"application/json"},
        data=json_data)
    # print(f"response from POST toy2 is {response3.json()}")
    id2 = response3.json()['id']
    assert response3.status_code == 201


def test_get_toy2():
    global id2, allToys
    response2 = requests.get(urlToys + '/' + id2)
    # print(f"response from GET toys {id2} is {response2.json()}")
    assert response2.status_code == 200
    assert_fields_equal(toy1, response2.json())

def test_get_all():
    global id1, id2
    response4 = requests.get(urlToys)
    all_toys = response4.json()
    assert response4.status_code == 200
    # assert that the collection returned contains toys with id1 and id2
    assert_collection_contains_field_values(all_toys, "id", [id1, id2])

# to see print statements, issue command: pytest -s