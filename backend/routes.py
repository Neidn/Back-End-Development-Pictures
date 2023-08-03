from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))


######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200


######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if not data:
        return {"message": "Internal server error"}, 500

    return jsonify(data), 200


######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    flag = False
    picture = None

    for p in data:
        if p["id"] == id:
            flag = True
            picture = p

    if flag:
        return jsonify(picture), 200
    # Return 404 if not found
    return {"message": "Picture not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    posted_data = request.get_json()

    if not posted_data:
        return {"message": "No data provided"}, 400

    # Check if posted_data exists in data
    for p in data:
        if p["id"] == posted_data["id"]:
            return {"message": f"picture with id {p['id']} already present"}, 302

    # Add the picture to data
    data.append(posted_data)

    # Return the picture
    return jsonify(posted_data), 201


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    posted_data = request.get_json()

    if not posted_data:
        return {"message": "No data provided"}, 400

    # Check id exists in data
    get_picture_by_id(id)

    # Update the data
    for i in range(len(data)):
        if data[i]["id"] == id:
            data[i] = posted_data
            break

    # Return the picture
    return jsonify(posted_data), 200


# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    get_picture_by_id(id)

    flag = False
    index = None
    # Delete the picture
    for i in range(len(data)):
        if data[i]["id"] == id:
            flag = True
            index = i
            break

    if not flag:
        return {"message": "Picture not found"}, 404

    del data[index]
    return {"message": f"Picture with id {id} deleted"}, 204
