from settings import *
import json
from flask import Flask, make_response, request
from datetime import datetime, timedelta


@app.route('/', methods=['GET'])
def get_item():
    request_data = request.get_json()  # getting data from client
    resp = make_response(f"The Cookie has been Set {request_data['itemname']}")
    resp.set_cookie('itemname', request_data['itemname'])
    return resp

@app.route('/', methods=['POST'])
def post_item():
    '''Function to add new movie to our database'''
    # timestring = "17:00-21:00,7:00-10:00,10:45-14:45"
    request_data = request.get_json()  # getting data from client
    timestring = request_data["timestring"]
    range_list = timestring.split(",")
    is_item_available = False
    current_time = request.cookies.get('itemname', None)
    item = request_data["item"]
    current_time = datetime.strptime(current_time, "%H:%M")
    if current_time:
        for time_range in range_list:
            sample = time_range.split("-")
            range1 = datetime.strptime(sample[0], "%H:%M")
            range2 = datetime.strptime(sample[1], "%H:%M")
            if(current_time.time()>=range1.time() and current_time.time()<=range2.time()):
                is_item_available = True
                break
        
        if is_item_available:
            response = Response(f"{item} available", 200, mimetype='application/json')
        else:
            response = Response(f"{item} Not available", 200, mimetype='application/json')
    else:
        resp = make_response(f"Cookie not set")
        return resp
    return response


if __name__ == "__main__":
    app.run(port=1234, debug=True)
