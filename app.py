from flask import Flask, render_template, Response, jsonify, request, redirect, url_for
import gunicorn
from camera import *

app = Flask(__name__)


headings = ("Name","Album","Artist")
df1 = music_rec()
df1 = df1.head(15)

def gen(camera):
    while True:
        global df1
        frame, df1 = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        # Retrieve user's mood from the submitted form
        mood = request.form['mood']

        # Process the user's mood (you can store it, analyze it, etc.)

        # Continue with the existing logic or redirect to the main route
        global df1
        print(df1.to_json(orient='records'))
        return render_template('index.html', headings=headings, data=df1)

    return render_template('quiz.html') 

@app.route('/')
def index():
    global df1
    print(df1.to_json(orient='records'))
    return render_template('index.html', headings=headings, data=df1)


@app.route('/t')
def gen_table():
    return df1.to_json(orient='records')

@app.route('/feedback')
def feedback():
    return render_template('feedback_form.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    feedback = request.form.get('feedback')
    
    # Handle the feedback, you can save it to a database or perform any desired action
    
    return render_template('feedback_confirmation.html')

@app.route('/start_quiz')
def start_quiz():
    # Logic to reset the quiz or any setup needed before starting
   return redirect(url_for('quiz'))



if __name__ == '__main__':
    app.debug = True
    app.run()

