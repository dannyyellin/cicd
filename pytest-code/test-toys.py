import requests
import json
import connectionController
from assertions import *

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

toy3 = {
    "name": "water toy",
    "descr": "boat to use in bathtub",
    "age": 5,
    "price": 37.00
}


urlToys = 'http://localhost:8001/toys'
global id1,id2

def assert_fields_equal(record1: dict, record2: any):
    if type(record2) != type(record1):  # check that record2 is also a dictionary
        print(f'Returned object is not of type {str(type(record1))}\n')
        print("----->  FAILED <----- assert_fields_equal")
        sys.stdout.flush()
        return False
    for field in record1.keys():
        if field not in record2:
            print(f'Expected field named "{field}" in returned object but it was missing. Returned object = {record2}\n')
            print("----->  FAILED <----- assert_fields_equal")
            sys.stdout.flush()
            return False
        if record1[field] != record2[field]:
            print(f'Field "{field}" in returned object: {record2[field]} does not match expected value: {record1[field]}')
            print("----->  FAILED <----- assert_fields_equal")
            sys.stdout.flush()
            return False
    print("++++++ passed assert_fields_equal")
    True


# def test_get_not_exists_word_id():
#     global id1
#     NOT_EXISTS_WORD_ID = 11235
#     response = connectionController.http_get(f"words/{NOT_EXISTS_WORD_ID}")
#     assert_status_code(response, status_code=404)
#     assert_ret_value(response, returned_value=0)

def test_post_toy1(toy1):
    global id1
    json_data = json.dumps(toy1)
    response = requests.post(urlToys,
        headers={"Content-Type":"application/json"},
        data=json_data)
    print("response from POST toy1 is ", response.json())
    id1 = response.json()['id']
    assert response.status_code == 201

def test_get_toy1():
    global id1
    response2 = requests.get(urlToys + '/' + id1)
    print(f"response from GET toys {id1} is {response2.json()}")
    assert response2.status_code == 200
    assert_fields_equal(toy1, response2.json())

# def get_all():

def test_post_toy2(toy1):
    global id2
    json_data = json.dumps(toy2)
    response3 = requests.post(urlToys,
        headers={"Content-Type":"application/json"},
        data=json_data)
    print(f"response from POST toy2 is {response3.json()}")
    id2 = response3.json()['id']
    assert response3.status_code == 201

# response4 = requests.get(urlToys)
# print("response from GET (ALL) toys", response4.json())
#
#
# response5= requests.get(urlToys+"?price=25.00")
# print("response from GET (ALL) toys with price = 25.00", response5.json())
#
# response6 = requests.delete(urlToys + '/' + id1)
# print(f"response from DELETE toy1 is {response6.text}")
#
# response7  = requests.get(urlToys)
# print("response from GET (ALL) toys", response7.json())
#
# json_data = json.dumps(toy3)
# response8 = requests.post(urlToys,
#                 headers={"Content-Type":"application/json"},
#                 data=json_data)
# print("response from POST toy3 is ", response8.json())
# id1 = response.json()['id']
#
# response9  = requests.get(urlToys)
# print("response from GET (ALL) toys", response9.json())



# response10= requests.get(urlToys+"?age=5")
# print("response from GET (ALL) toys with age = 5", response10.json())