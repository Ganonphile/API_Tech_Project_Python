import json
import flask

app = flask.Flask(__name__)

cities = []

weights = [
   
]

with open("data/cities.json", 'r') as data_file:
    data = json.load(data_file)
    
@app.route("/city/<cityid>", methods=['GET'])
def return_city(cityid):
    if cityid.isdigit():
        for city in data:
            if city["id"] == int(cityid):
                return(json.dumps(city))
            else:
                # This should generate an error code.
                pass
    else:
        # This should generate an error code.
        pass

@app.route("/rank", methods=['POST'])
def city_weights():
    city_scores = []

    if flask.request.headers['Content-type'] == 'application/json':
        weights = flask.request.json
        weighted_cities = weigh_city(weights["weights"])
        return(json.dumps(weighted_cities))
        
    else:
        # Generate an error code.
        pass

def weigh_city(weights):
    # Helper function designed to make code a little clearer.
    weight_walk = weights["walkability"]
    weight_job = weights["job_growth"]
    weight_green = weights["green_space"]
    weight_taxes = weights["taxes"]
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
    
if __name__ == '__main__':
    app.run()