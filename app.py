from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import json, traceback
from get_data import get_data
from get_spectrum import get_spectrum, make_spectrum_math_obj
from time import sleep

app = Flask(__name__, template_folder='./')
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = '12345678'
socketio = SocketIO(app)

@app.route('/ping')
def index():
    return {"message":"pong"}

@app.route('/', defaults={'file': 'index.html'})
def serve_results(file):
    # Haven't used the secure way to send files yet
    return render_template(file)

@socketio.on('simulation:start')
def simulation():
    emit('message', {"type":"simulation:started", "data": True })
    simulation_data = get_data()
    spectrum_math = make_spectrum_math_obj()
    for i in range(len(simulation_data)):
        # send raw data
        end_index = i+50
        data_slice = simulation_data[i:end_index]
        emit("message", {"type":"simulation:data:raw", "data":data_slice})
        # send sepctrum data
        waves_spectrum_data = get_spectrum(data=list(map(lambda x: x['c1'], data_slice)), spectrum_math=spectrum_math)
        for i in range(len(waves_spectrum_data)):
            alpha_theta_ratio = waves_spectrum_data[i].alpha_raw/ waves_spectrum_data[i].theta_raw
            emit("message", {"type":"simulation:data:alpha-theta-ratio", "data":alpha_theta_ratio})
        i = end_index
        sleep(0.2)

@socketio.on('real-deal')
def simulation():
    pass

@socketio.on('connect_event')
def connected_msg(msg):
    emit('server_response', {'data': msg['data']})


if __name__ == '__main__':
    socketio.run(app, debug=True, host='127.0.0.1', port=5000)