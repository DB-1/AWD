# import necessary libraries:
import jwt as jwt
from flask import Flask, jsonify, request, Response, make_response
import jwt
import datetime
from functools import wraps
from flaskext.mysql import MySQL

# define the name of flask application:
testRestServer = Flask(__name__)
testRestServer.config['SECRET_KEY'] = 'simplekey'

# variable for MySQL
mysql = MySQL()

# standard for DB
testRestServer.config['MYSQL_DATABASE_USER'] = '**'
testRestServer.config['MYSQL_DATABASE_PASSWORD'] = '**'
testRestServer.config['MYSQL_DATABASE_DB'] = '**'

# YSJ server:
testRestServer.config['MYSQL_DATABASE_HOST'] = 'cs2s.yorkdc.net'


# Local server:
# testRestServer.config['MYSQL_DATABASE_HOST'] = 'localhost'

# Not necessary, but sometimes needed:
# testRestServer.config['MYSQL_DATABASE_PORT'] = 3306
# testRestServer.config['MYSQL_DATABASE_CHARSET'] = 'utf8'

mysql.init_app(testRestServer)

# variables for DB
conn = mysql.connect()
cursor = conn.cursor()

def read_token(f):
    @wraps(f)
    def tokenised(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'response': 'Token is missing'}), 403
        try:
            data = jwt.decode(token, testRestServer.config['SECRET_KEY'])
        except:
            return jsonify({'response': 'Token is invalid'}), 403
        return f(*args, **kwargs)

    return tokenised


# Needed for access the server from the restClient
@testRestServer.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@testRestServer.route("/dbMap", methods=['GET', 'POST'])
def getData():
    cursor.execute("SELECT * FROM markers ")
    return jsonify(cursor.fetchall())

# root request that return a simple string
@testRestServer.route("/")
def testHello():
    if request.authorization and request.authorization.username == 'test2' and request.authorization.password == 'test':

        return "Hello"
    else:
        return make_response('Authorization failed', 401, {'WWW-Authenticate': 'Basic realm ="Login Required"'})

    # /gettoken request:


@testRestServer.route("/gettoken")
def gettoken():
    if request.authorization and request.authorization.username == 'test2' and request.authorization.password == 'test':
        token = jwt.encode({'user': request.authorization.username,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)},
                           testRestServer.config['SECRET_KEY'])
        return jsonify({'token': str(token)})
    else:
        return make_response('Authorization failed', 401, {'WWW-Authenticate': 'Basic realm ="Login Required"'})




@testRestServer.route("/havetoken")
@read_token
def havetoken():
    return jsonify({'response': 'Welcome Authorized User'})


if __name__ == '__main__':
    # Run YSJ server:
    testRestServer.run(host='0.0.0.0', port=**, debug=True)
# Run Local server
# testRestServer.run(host='localhost', port=5032, debug=True)
