from flask import Flask, render_template, Response,jsonify
from camera import PlantCamera
app = Flask(__name__)
import atexit
import time
from threading import Thread
from globals import plant_data
from light import GrowLight

@app.route("/")

def index():
    return render_template('index.html')

def gen(camera):
    """Video streaming generator function."""
    yield b'--frame\r\n'
    while True:
        frame = camera.get_frame()
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(plantCam),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/data')
def get_data():
    return jsonify(plant_data)


@app.route('/light/increase', methods=['POST'])
def increase_light():
    growLight.increaseDutyCycle()
    return jsonify({'status': 'success', 'dutyCycle': growLight.dutyCycle})

@app.route('/light/decrease', methods=['POST'])
def decrease_light():
    growLight.decreaseDutyCycle()
    return jsonify({'status': 'success', 'dutyCycle': growLight.dutyCycle})


# @app.route('/pump_on', methods=['POST'])
# def pump_on():
#     print ("Pump remotely on")
#     waterPump.pump_on()
#     return jsonify({'status': 'success', 'pumpStatus': waterPump.state})


@atexit.register
def shutdown_camera():
    print("Shutting down camera...")
    plantCam.close()


def start_flask_thread(camera,light):
    global plantCam,growLight
    plantCam = camera
    growLight = light
    thread = Thread(target=lambda: app.run(threaded=True))
    thread.daemon = True
    thread.start()

# if __name__ == "__main__":
   
#     app.run()