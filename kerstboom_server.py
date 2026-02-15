from flask import Flask, render_template, request
from start_effect import *
import json
import plotly
import sys

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html', effects = effects.keys())

@app.route('/effect/<effect>', methods=['GET'])
def show_effect(effect):
    # start_effect(effect)
    fig = effects[effect].run_preview(coords, LIGHTS_COUNT)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('effect.html', 
                           name=effect, 
                           message=effects[effect].message, 
                           graphJSON=graphJSON, 
                           colors=COLORS.keys(),
                           default_colors=effects[effect].default_colors)

@app.route('/effect/turnoff', methods=['GET'])
def turnoff():
    start_effect("turnoff")
    return "<p>Effect turned off!</p>"

@app.route('/boom/<effect>', methods=['POST'])
def boom(effect):
    colors = []
    for i in range(10):
        color = request.form.get(str(i))
        if color == None:
            break
        colors.append(color)
    start_effect(effect, colors)
    return json.dumps({'success':True, 'data': request.form}), 200, {'ContentType':'application/json'}

@app.route('/preview/<effect>', methods=['POST'])
def preview(effect):
    colors = []
    for i in range(10):
        color = request.form.get(str(i))
        if color == None:
            break
        colors.append(color)
    return json.dumps({'success':True, 'data': request.form}), 200, {'ContentType':'application/json'}
        
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
