from flask import Flask, jsonify, request, Response
from flask.views import MethodView
from models import Advertisment, Session
from errors import HttpError
from schema import validate, CreateAdvertisment, UpdateAdvertisment

app = Flask("hello_world")

def get_Advertisment_by_id(Advertisment_id: int):
    advertisment: Advertisment = request.session.get(Advertisment, Advertisment_id)
    if advertisment is None:
        raise HttpError(404, "not found")
    return advertisment


def delete_Advertisment_by_id(Advertisment_id: int):
    advertisment = get_Advertisment_by_id(Advertisment_id)
    request.session.delete(advertisment)
    request.session.commit()

def add_Advertisment(advertisment: Advertisment):
    request.session.add(advertisment)
    request.session.commit()

@app.before_request
def before_request():
    session = Session()
    request.session = session
    pass

@app.after_request
def after_request(response: Response):
    request.session.close()
    return response

@app.errorhandler(HttpError)
def error_errorhandler(error):
    json_response = jsonify({"status": "error", "message": error.message})
    json_response.status_code = error.code
    return json_response   

class AdvertismentView(MethodView):
    def get(self, Advertisment_id: int):
        advertisment = get_Advertisment_by_id(Advertisment_id)
        if advertisment is None:
            response = jsonify({"error": "not found"})
            response.status_code = 404
            return response
        return jsonify(advertisment.dict)

    def post(self):
        validated_data = validate(CreateAdvertisment, request.json)
        advertisment = Advertisment(**validated_data)
        add_Advertisment(advertisment)
        return jsonify(advertisment.id_dict)

    def delete(self, Advertisment_id: int):
        delete_Advertisment_by_id(Advertisment_id)
        return jsonify({"status": "deleted"})

    def patch(self, Advertisment_id: int):
        advertisment = get_Advertisment_by_id(Advertisment_id)
        validated_data = validate(UpdateAdvertisment, request.json)
        for field, value in validated_data.items():
            setattr(advertisment, field, value)
        add_Advertisment(advertisment)
        return jsonify(advertisment.id_dict)


Advertisment_view = AdvertismentView.as_view("Advertisment")

app.add_url_rule(
    "/Advertisment/<int:Advertisment_id>", view_func=Advertisment_view, 
    methods=["GET", "DELETE", "PATCH"])
app.add_url_rule("/Advertisment", view_func=Advertisment_view, methods=["POST"])

app.run()