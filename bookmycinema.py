from flask_cors import CORS
from flask import Flask, jsonify, request
import pymongo
import datetime

connection_url = 'mongodb+srv://kashyapurvi:popxo1234@cluster0.cei5i.mongodb.net/<dbname>?retryWrites=true&w=majority'
app = Flask(__name__)
CORS(app)
client = pymongo.MongoClient(connection_url)


DB = client.get_database('book_cinema')
ticket = DB.ticket
datastore = DB.datastore

ticket.create_index("currtime", expireAfterSeconds=8*3600)


@app.route('/book-my-cinema', methods=['POST'])
def bookmycinema():
    name = request.json["name"]
    phone = request.json["phone"]
    showtime = request.json["showtime"]
    if showtime == 2:
        queryobj = {"showtime": 2}
        c2= DB.ticket.count_documents(queryobj)

        if c2 < 20:
            queryobj = {"cid": "tid"}
            que = datastore.find_one(queryobj)
            count = que["tid"]
            
            queryobj = {
                'name': name,
                '_id': count+1,
                'phone': phone,
                'showtime': 2,
                'currtime':datetime.datetime.utcnow()
            }
            que = ticket.insert_one(queryobj)
            
            queryobj = {"cid": "tid"}
            updateobject = {"tid": count+1}
            que = datastore.update_one(queryobj, {'$set': updateobject})

        else:
            return "TICKETS FOR 2PM UNAVAILABLE"

    elif showtime == 10:
        queryobj = {"showtime": 10}
        c10=DB.ticket.count_documents(queryobj)
        if c10 < 20:
            queryobj = {"cid": "tid"}
            que = datastore.find_one(queryobj)
            count = que["tid"]

            queryobj = {
                'name': name,
                '_id': count+1,
                'phone': phone,
                'showtime': 10,
                'currtime':datetime.datetime.utcnow()
            }
            que = ticket.insert_one(queryobj)

            queryobj = {"cid": "tid"}
            updateobject = {"tid": count+1}
            que = datastore.update_one(queryobj, {'$set': updateobject})

        else:
            return "TICKETS FOR 10PM UNAVAILABLE"

    else:
        return "SORRY! WE ARE AVAILABLE ONLY FOR 10PM AND 2PM. PLEASE SELCT A VALID SHOW TIMING"

    return "QUERY INSERTED SUCCESSFULLY"

@app.route('/view-user-details/id/<value>/', methods=['GET'])
def user(value):
    queryObj = {"_id": int(value)} 
    que = ticket.find(queryObj)
    result = {}
    i = 0
    for j in que:
        result[i] = j
        i = i+ 1
    return jsonify(result)


@app.route('/ticket-detail/showtime/<value>/', methods=['GET'])
def view(value):
    queryObj = {"showtime": int(value)}
    que = ticket.find(queryObj)

    result = {}
    i = 0
    for j in que:
        result[i] = j
        i = i+ 1
    return jsonify(result)




@app.route('/update-detail/id/<idvalue>/<newval>', methods=['GET'])
def updatedetail(idvalue, newval):

    queryObj = {"_id": int(idvalue)}  
    updateObj = {"showtime": int(newval)}  
    Query = ""
    newval = int(newval) 
    if newval == 10:
        c10=DB.ticket.count_documents({"showtime":10})
        if c10 < 20:
            Query = ticket.update_one(queryObj, {'$set': updateObj})   
        else:
            return "SORRY! WE ARE ALREADY FULL FOR 10PM"

    elif newval == 2:
        c2=DB.ticket.count_documents({"showtime":2})
        if c2 < 20:
            Query = ticket.update_one(queryObj, {'$set': updateObj})
        else:
            return "SORRY! WE ARE ALREADY FULL FOR 2PM"

    if Query.acknowledged:
        return "UPDATED SUCCESSFULLY"
    else:
        return "UPDATION UNSUCCESSFUL"    


@app.route('/delete/', methods=['POST'])
def delete():
    _id = request.json["_id"]   
    queryObj = {
        '_id': _id,
    }
    ticket.delete_one(queryObj) 

    return "DELETED SUCCESSFULLY"





if __name__ == '__main__':
    app.run(debug=True)
