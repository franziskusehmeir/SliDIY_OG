from flask import Flask, render_template_string, request 
import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
coil_A_2_pin = 4 # A\ gruen-weiss
coil_B_1_pin = 17 # B rot-lila
coil_A_1_pin = 23 # A schwarz-schwarz
coil_B_2_pin = 24 # B\ blau-grau

# anpassen, falls andere Sequenz
StepCount = 4
Seq = list(range(0, StepCount))
Seq[0] = [1,0,1,0]
Seq[1] = [0,1,1,0]
Seq[2] = [0,1,0,1]
Seq[3] = [1,0,0,1]

GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)

app = Flask(__name__)
 
#HTML 

TPL = '''

<html>

    <head><title>SliDIY</title></head>

    <body>

    <h2>SliDIY</h2>

        <form method="POST" action="test">

            <label for="steps">Steps(50 = 360°):</label><br>
            <input type="number" id="steps" name="steps" value=50><br>
            
            <label for="delay">Delay in ms:</label><br>
            <input type="number" id="delay" name="delay" value=5><br>
            
            <br>
            <input type="submit" value="submit" />

        </form>

    </body>

</html>

'''

def setStep(w1, w2, w3, w4):
    GPIO.output(coil_A_1_pin, w1)
    GPIO.output(coil_A_2_pin, w2)
    GPIO.output(coil_B_1_pin, w3)
    GPIO.output(coil_B_2_pin, w4)
 
def forward(delay, steps):
    for i in range(steps):
        for j in range(StepCount):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)
 
def backwards(delay, steps):
    for i in range(steps):
        for j in reversed(range(StepCount)):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)
            
 

@app.route("/")

def home():

    return render_template_string(TPL)
 

@app.route("/test", methods=["POST"])

def test():

    # Get slider Values

    delay = request.form["delay"]

    print(float(delay))
    
    steps = request.form["steps"]

    print(int(steps))

    if(float(steps) > 0):
        forward(int(delay) / 1000.0, int(steps))
        print("rotate clockwise")
        
    if(float(steps) < 0):
        backwards(int(delay) / 1000.0, int(steps)*(-1))
        print("rotate anti-clockwise")
        
    setStep(0,0,0,0)
    

    return render_template_string(TPL)

 

# Run the app on the local development server

if __name__ == "__main__":

    app.run()
