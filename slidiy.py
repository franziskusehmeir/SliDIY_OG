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
# eine ganze Sequenz entspricht 0.08cm
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

# Slider-Laenge in cm
sliderLength = 55

# Anzahl an Steps fuer eine ganze Kamerafahrt
completeSteps = sliderLength/0.08

app = Flask(__name__)
 
#HTML 

TPL = '''

<html>

    <head>
        <title>SliDIY</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='styles/style.css') }}">
        
    </head>

    <body>

    <div>

    <h2>SliDIY</h2>

        <form method="POST" action="run">
            
            <p>Distance: <span id="value"></span>cm</p>
            <input type="range" id="distance" name="distance" min="-55" max="55" value="0"><br>
            
            <label for="time">Time in s:</label><br>
            <input type="number" id="time" name="time" min=1 value=5><br>
            
            <br>
            <input type="submit" value="run" />

        </form>
    </div>
    
        <script>
            var slider = document.getElementById("distance");
            var output = document.getElementById("value");

            output.innerHTML = slider.value;

            slider.oninput = function() {
                output.innerHTML = this.value;
            }
        </script>
        
    </body>

</html>

'''

# Zustand der Pins setzen
def setStep(w1, w2, w3, w4):
    GPIO.output(coil_A_1_pin, w1)
    GPIO.output(coil_A_2_pin, w2)
    GPIO.output(coil_B_1_pin, w3)
    GPIO.output(coil_B_2_pin, w4)
 
def acceleration(delay, steps, currentStep):
    acc_time=0.01-delay
    acc_steps=steps/9
    acc_delay=acc_time/acc_steps
    if(delay<0.01 and currentStep < acc_steps):
        time.sleep(delay+(acc_delay*(acc_steps-currentStep)))
    elif(delay<0.01 and currentStep > steps-acc_steps):
        time.sleep(delay+(acc_delay*(acc_steps-(steps-currentStep))))
    else:
        time.sleep(delay)
        
    
 
def forward(delay, steps):
    for i in range(steps):
        for j in range(StepCount):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            acceleration(delay, steps, i)
 
def backwards(delay, steps):
    for i in range(steps):
        for j in reversed(range(StepCount)):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            acceleration(delay, steps, i)
            
 

@app.route("/")

def home():

    setStep(0,0,0,0)

    return render_template_string(TPL)
 

@app.route("/run", methods=["POST"])

def run():

    setStep(0,0,0,0)

    # Get slider Values
    distance = request.form["distance"]
    
    time = int(request.form["time"])
    
    print(int(distance))

    if(int(distance) > sliderLength):
        distance=0
        
    steps = int(distance)/0.08
    
    delay = 0
    
    # /4 damit die richtige Zeit rauskommt
    if(steps != 0):
        delay = time/steps/4
    
    if(delay < 0):
        delay = -delay
    
    if(delay<0.003):
        delay = 0.003

    print(delay)

    print(int(steps))

    if(float(steps) > 0):
        forward(delay, int(steps))
        print("rotate anti-clockwise")
        
    if(float(steps) < 0):
        backwards(delay, int(steps)*(-1))
        print("rotate clockwise")
        
    setStep(0,0,0,0)
    

    return render_template_string(TPL)

 

# Run the app on the local development server

if __name__ == "__main__":

    app.run()
