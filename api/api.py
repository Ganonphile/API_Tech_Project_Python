import json
import flask

app = flask.Flask(__name__)

error = {}
error["Errors"] = []

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
    key_verify(weights)

    # We don't need to perform a value check, as if its not a dictionary, its an invalid
    # json object
    
    weight_walk = key_check(weights, "walkability")
    key_verify(weight_walk)
    print(type(weight_walk))

    weight_job = key_check(weights, "job_growth")
    key_verify(weight_job)
    value_check(weight_job)
    
    weight_green = key_check(weights, "green_space")
    key_verify(weight_green)
    value_check(weight_green)
    
    weight_taxes = key_check(weights, "taxes")
    key_verify(weight_taxes)
    value_check(weight_taxes)
    
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

def key_verify(result):
    if result is False:
        error_return("Key is invalid")

def value_check(value):
    if type(value) is not float:
        error_return("Value is not float")

def error_return(message):
    print("Made it here", message)
    error["Errors"] = [message]
    return json.dumps(error), 400


if __name__ == '__main__':
    app.run()