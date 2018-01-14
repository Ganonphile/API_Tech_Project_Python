import json
import flask

app = flask.Flask(__name__)

error = {}

with open("data/cities.json", 'r') as data_file:
    data = json.load(data_file)
    
@app.route("/city/<cityid>", methods=['GET'])
def return_city(cityid):
    if cityid.isdigit():
        for city in data:
            if city["id"] == int(cityid):
                return json.dumps(city), 200
            else:
                error["Errors"] = ["No city with id '" + cityid + "'"]
                return json.dumps(error), 400
    else:
        error["Errors"] = ["City ID was not an integer, it was '" + cityid + "'"]
        return json.dumps(error), 400

@app.route("/rank", methods=['POST'])
def city_weights():
    city_scores = []

    if flask.request.headers['Content-type'] == 'application/json':

        try:
            weights = flask.request.json
        except:
            error["Errors"] = ["Information provided was not in json format"]
            return json.dumps(error), 400

        weighted_cities = weigh_city(weights)
        return(json.dumps(weighted_cities))
        
    else:
        error["Errors"] = ["Content was not of type 'application/json'"]
        return json.dumps(error), 400

def weigh_city(weights):
    # Helper function designed to make code a little clearer.
    # Also catches more errors.
    
    weights = key_check(weights, "weights")
    if weights == False:
        error["Errors"] = ["Key is invalid"]
        return json.dumps(error), 400

    # We don't need to perform a value check, as if its not a dictionary, its an invalid
    # json object
    
    try:
        weight_walk = weights["walkability"]
    except KeyError:
        return json.dumps(error), 400

    weight_job = key_check(weights, "job_growth")
    if weight_job is False:
        error["Errors"] = ["Key is invalid"]
        return json.dumps(error), 400
    
    weight_green = key_check(weights, "green_space")
    if weight_green is False:
        error["Errors"] = ["Key is invalid"]
        return json.dumps(error), 400
    
    weight_taxes = key_check(weights, "taxes")
    if weight_taxes is False:
        error["Errors"] = ["Key is invalid"]
        return json.dumps(error), 400
    
    unsorted_cities = []
    
    for city in data:
        walkability = float(city["scores"]["walkability"])*weight_walk
        job_growth = float(city["scores"]["job_growth"])*weight_job
        green_space = float(city["scores"]["green_space"])*weight_green
        taxes = float(city["scores"]["taxes"])*weight_taxes
                      
        overall_score = format(walkability + job_growth + green_space + taxes, '.2f')
        updated_city = city
        updated_city.update({"overall_score":overall_score})
        unsorted_cities.append(updated_city)

    sorted_data = sorted(data, key=lambda key: key["overall_score"], reverse=True)
    return sorted_data

def key_check(dictionary, key):
    try:
        result = dictionary[key]
    except:
        return False
    return result

if __name__ == '__main__':
    app.run()