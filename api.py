from cgitb import reset
import os, json
import pandas as pd
from flask import Flask, jsonify
from flask_restful import  Api, reqparse,Resource
from flask_cors import CORS, cross_origin
from recommend import recommend_from_mood,recommend
import authorization
from flask_jsonpify import jsonpify


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Require a parser to parse our POST request.
parser = reqparse.RequestParser()
parser.add_argument("track_ID")
parser.add_argument("mood")

api = Api(app)

class Recommend(Resource):
  # sanity check route
  @app.route('/recommend/', methods=['POST'])
  def post():
    args = parser.parse_args()

    df = pd.read_csv("valence_arousal_dataset.csv")
    df["mood_vec"] = df[["valence", "energy"]].values.tolist()
    sp = authorization.authorize()
    track = str(args["track_ID"])
    list = recommend(track_id= track, ref_df = df, sp = sp, n_recs = 4)
    
    data_dict = dict()
    for col in list.columns:
      data_dict[col] = list[col].values.tolist()
    response =  jsonify(data_dict)
    response.headers.add("Access-Control-Allow-Origin", "*")
    

    return response


class Mood(Resource):
  # sanity check route
  @app.route('/mood/', methods=['POST'])
  def postMood():
    args = parser.parse_args()

    df = pd.read_csv("valence_arousal_dataset.csv")
    df["mood_vec"] = df[["valence", "energy"]].values.tolist()
    sp = authorization.authorize()
    mood = str(args["mood"])
    list = recommend_from_mood(mood, ref_df = df,  n_recs = 10)

    data_dict = dict()
    for col in list.columns:
      data_dict[col] = list[col].values.tolist()
    response =  jsonify(data_dict)
    response.headers.add("Access-Control-Allow-Origin", "*")
    

    return response

api.add_resource(Mood, "/mood/")

api.add_resource(Recommend, "/recommend/")
if __name__ == "__main__":
  app.run(debug=True)