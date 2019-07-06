import os
from flask import Flask, render_template, request, jsonify

# class to represent rooms
class Room:
    def __init__(self, name, isOccupied):
        self.name = str(name)
        self.isOccupied = bool(isOccupied)

# array to contain room instances
rooms = []

# object for python server application
app = Flask(__name__)

# set the secret key
app.secret_key = "8975917845yhiWUEFHYDFU*(#@!$73RYUIAWGDF"

# root page
@app.route("/")
def index():
    return render_template("index.html")

# http route for setting status of a room (i.e. whether or not it is occupied) 
@app.route("/setRoomStatus")
def setRoomStatus():

    # get remote input from an HTTP "post" request
    if request.method == "POST":
        req_name = str(request.form.get("name"))
        req_isOccupied = bool(request.form.get("isOccupied"))
    
    # get remote input from an HTTP "get" request
    if request.method == "GET":
        req_name = str(request.args.get("name"))
        req_isOccupied = bool(request.args.get("isOccupied"))

    # variable to indicate whether or not room already exists in "rooms" array
    isRoomAlreadyInArray = False
    
    # set the status for the room based on remote input if the room is already
    # in the "rooms" array
    for room in rooms:
        if room.name == req_name:
            room.isOccupied = req_isOccupied
            isRoomAlreadyInArray = True

    # add room and status to the "rooms" array if it is not already in array
    if not isRoomAlreadyInArray:
        rooms.append(Room(req_name, req_isOccupied))

    # construct mesasge to be returned in JSON package
    returnMessage = "Room " + req_name + " is now listed as "
    if req_isOccupied == True:
        returnMessage += "occupied"
    elif req_isOccupied == False:
        returnMessage += "not occupied"
    else:
        # req_isOccupied should be either True of False; if not, 
        # something went wrong, so notify machine making HTTP request
        returnMessage = "Oh no! Something went wrong! Bad input?"
        return jsonify(success = False, returnMessage = returnMessage)
    

    # send back a JSON object
    return(
        jsonify(
            success = True,
            returnMessage = returnMessage
        )
    )


# configure server
server_address = "0.0.0.0"
port_number = 8080

# run server
if __name__ == "__main__":
    app.run(host = os.getenv('IP', server_address), 
            port = int(os.getenv('PORT', port_number)))
