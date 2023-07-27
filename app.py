from flask import Flask, render_template, request, redirect, url_for
import boto3

app = Flask(__name__)

# Sample list of tasks (messages)
tasks = []

# AWS SNS Client
sns_client = boto3.client('sns', region_name='us-west-2')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        feedback = request.form['feedback']
        if send_notification(feedback):
            tasks.append(feedback)
            return redirect(url_for('success'))
        else:
            return redirect(url_for('error'))

    return render_template('index.html', tasks=tasks)

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/error')
def error():
    return render_template('error.html')

def send_notification(feedback):
    topic_arn = 'YOUR_SNS_TOPIC_ARN'

    try:
        # Publish the feedback as a push notification
        sns_client.publish(
            TopicArn=topic_arn,
            Message=feedback,
            Subject='Doctor Feedback'
        )
        return True
    except Exception as e:
        print(f"Error sending notification: {e}")
        return False

if __name__ == '__main__':
    app.run(debug=True)
