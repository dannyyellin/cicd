# This is example REST API server code for lecture: topic-2 REST APIs
# It uses Flask to build a RESTful service in Python.
# A good introduction is https://towardsdatascience.com/the-right-way-to-build-an-api-with-python-cd08ab285f8f
# See also https://dzone.com/articles/creating-rest-services-with-flask
# To run this program, in terminal window issue the cmd:
#   python3 toys.py
# alternatively, comment out "app.run..." cmd in __main__ and issue the following cmds
#   export FLASK_APP-"toys.py"
#   flask run --port 8000     (or whatever port you want to run on.  if no "--port" option specified, it is port 5000)
# flask will return the IP and port the app is running on
# you must install the packages Flask before running this program

# The resources are:
# /toys          This is a collection resource
# /toys/{id}     This is the toy given by the identifier id.  id is a UUID represented as a string.
# A toy is of the form:
# {
#     'id': 'string',
#     'name':'string',
#     'descr': 'string',
#     'age': integer,
#     'price': 'float',
#     'features': 'array'
# }
# age is the minimal child age fit for this toy.
# 'features' is an array of strings, where each string describes a different feature of the toy.
# See https://json-schema.org/learn/getting-started-step-by-step on how to define JSON schema

from flask import Flask, jsonify, request, make_response
import json
# from genID import genID    # generates a unique string ID


global N
N = 0

def genID():
    global N
    N += 1
    return(str(N))


app = Flask(__name__)  # initialize Flask
Toys = {}


@app.route('/toys', methods=['POST'])
def addToy():
    print("POST toys")
    try:
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return jsonify("{error: Expected application/json}"), 415  # 415 Unsupported Media Type
        data = request.get_json()
        # Check if required fields are present
        required_fields = ['name', 'age', 'price']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Malformed data"}), 400
        newID = genID()      # returns string ID
        if 'features' not in data:
            features = []
        else:
            features = data['features']
        if 'descr' not in data:
            descr = "Not Available"
        else:
            descr = data['descr']
        toy = {
            'id':newID,
            'name':data['name'],
            'descr':descr,
            'age':data['age'],
            'price':data['price'],
            'features':features
        }
        Toys[newID] = toy
        response_data = {"id":newID}
        return jsonify(response_data),201
    except Exception as e:
        print("Exception: ", str(e))
        return jsonify({"server error":str(e)}),500

# The following is a different version of the POST toys implementation.   The only difference is that thr url of the
# newly created response is included in the 'location' attribute of the responser header.   The HTTP says that the
# resource url, or relative url, of a new resource can be returned in this fashion.
# see https://www.rfc-editor.org/rfc/rfc9110#field.location   I am including it here just for reference.
@app.route('/toys', methods=['POST'])
def addToy2():
    print("POST toys")
    try:
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return jsonify({"error":"Expected application/json media type"}), 415  # 415 Unsupported Media Type
        data = request.get_json()
        # Check if required fields are present
        required_fields = ['name','age','price']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Malformed data"}), 400
        newID = genID()   # returns unique string ID
        if 'features' not in data:
            features = []
        else:
            features = data['features']
        if 'descr' not in data:
            descr = "Not Available"
        else:
            descr = data['descr']
        toy = {
            'id': newID,
            'name':data['name'],
            'descr': descr,
            "age": data["age"],
            'price': data['price'],
            'features': features
        }
        Toys[newID] = toy
        data = {"id": newID}
        response = make_response(data,201)
        response.headers['Location'] = f'/toys/{newID}'
        return response
    except Exception as e:
        print("Exception: ", str(e))
        return jsonify({"server error":str(e)}),500


@app.route('/toys', methods=['GET'])
def getToys():
    try:
        return list(Toys.values()), 200
    except Exception as e:
        print("Exception: ", str(e))
        return jsonify({"server error":str(e)}),500


@app.route('/toys/<string:toyid>', methods=['GET'])
def getToy(toyid):
    print("GET toys")
    try:
        toy = Toys[toyid]
    except KeyError:
        print("GET request error: No such ID")
        return jsonify({"error":"Not found"}), 404
    except Exception as e:
        print("Exception: ", str(e))
        return jsonify({"server error":str(e)}),500
    return jsonify(toy), 200



@app.route('/toys/<string:toyid>', methods=['DELETE'])
def delToy(toyid):
    print("DELETE toys")
    try:
        del Toys[toyid]
        return '', 204
    except KeyError:
        print("GET request error: No such ID")
        return jsonify({"error":"Not found"}), 404
    except Exception as e:
        print("Exception: ", str(e))
        return jsonify({"server error":str(e)}),500


@app.route('/toys/<string:toyid>', methods=['PUT'])
def update(toyid):
    print("PUT toys")
    try:
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return jsonify({"error":"Expected application/json media type"}), 415  # 415 Unsupported Media Type
        data = request.get_json()
        # Check if required fields are present
        required_fields = ['name','age','price']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Malformed data"}), 400
        if 'features' not in data:
            features = []
        else:
            features = data['features']
        if 'descr' not in data:
            descr = "No description Available"
        else:
            descr = data['descr']
        if not Toys[toyid]:
            print("PUT error:No such ID")
            # no toy of this id exists
            return jsonify({"error":"Not found"}), 404
        toy = {
            'id': toyid,
            'name':data['name'],
            'descr': descr,
            "age": data["age"],
            'price': data['price'],
            'features': features
        }
        Toys[toyid] = toy
        response_data = {"id": toyid}
        return jsonify(response_data), 200
    except Exception as e:
        print("Exception: ", str(e))
        return jsonify({"server error":str(e)}),500


if __name__ == '__main__':
    print("running toys server")
    # run Flask app.   default part is 5000
    app.run(host='0.0.0.0', port=8000, debug=True)
