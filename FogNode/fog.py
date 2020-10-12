from flask import Flask, request
from flask_restful import Api


# db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__)
api = Api(app)

sensors = [0, 0, 0, 0, 0, 0]


@app.route('/', methods=["GET"])
def usage():
    return {'Welcome to the progetto ammazzata!': 'bah'}


@app.route('/all', methods=["GET"])
def get_all():
    return {'sensors': sensors}


@app.route('/update', methods=["POST"])
def update():
    try:

        sensor_num = request.form['num']
        sensor_val = request.form['val']

        sensors[int(sensor_num)] = int(sensor_val)

        print(sensor_num)

        return {'DONE': "OK"}

    except Exception as e:

        return {'Exception': e.args}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080')
