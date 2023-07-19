from flask import Flask
from indy_utils import indydcp_client as client
from time import sleep
from pyModbusTCP.client import ModbusClient
import time 
app = Flask(__name__)

SERVER_HOST = "192.168.0.176"
SERVER_PORT = 502

robot_ip = "192.168.0.176"  # Robot (Indy) IP
robot_name = "NRMK-Indy7"  # Robot name (Indy7)

modbus_client = ModbusClient(host=SERVER_HOST, port=SERVER_PORT, auto_open=True)
# Create class object
indy = client.IndyDCPClient(robot_ip, robot_name)


@app.route('/')
def index():
    return '''<!doctype html>
    <html>
        <head>
            <style>
                /* Add custom styles for the buttons */
                .button-container {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
                .button-container form {
                    margin: 20px;
                }
                .button-container input[type="submit"] {
                    width: 200px;
                    height: 60px;
                    font-size: 24px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    cursor: pointer;
                }
                .button-container input[type="submit"]:hover {
                    background-color: #45a049;
                }
            </style>
        </head>
        <body>
            <div class="button-container">
                <form method="post" action="/start_program">
                    <p><input type="submit" value="START" /></p>
                </form>
                <form method="post" action="/stop_program">
                    <p><input type="submit" value="STOP" /></p>
                </form>
            </div>
        </body>
    </html>'''

@app.route('/start_program', methods=['POST'])
def start_program():
    indy.connect()
    indy.set_default_program(7)
    indy.start_default_program()
    return 'Started the default program.'

@app.route('/stop_program', methods=['POST'])
def stop_program():
    indy.connect()
    indy.stop_current_program()
    indy.disconnect()
    return 'Stopped the default program.'
try:
    
    modbus_client.open()
    print("\nOpen Robot Status\n")

    try:

        i = indy.connect()
        while(True):
            if not i :
                print('connect fail')
                time.sleep(1)
                continue
            if i :
                print('connect')
                break

        app.run(debug=True)
    finally:
        indy.disconnect()
finally:
    modbus_client.close()
    print("Close RobotStatus")

# if __name__ == '__main__':
#     app.run(debug=True)
    