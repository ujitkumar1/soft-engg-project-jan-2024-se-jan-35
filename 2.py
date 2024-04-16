from flask import Flask, request, jsonify, redirect
from google_auth_oauthlib.flow import Flow
import google.oauth2.credentials

app = Flask(__name__)

messages = {}

CLIENT_SECRETS_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/chat.bot']
PORT = 8080

flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri=f'http://localhost:{PORT}/oauth2callback'
)

@app.route('/')
def index():
    authorization_url, _ = flow.authorization_url(prompt='consent')
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    return jsonify(token=credentials.token)

@app.route('/messages', methods=['POST'])

@app.route('/messages', methods=['POST'])
def send_message():
    data = request.json
    thread_id = data.get('threadId')
    text = data.get('text')
    urgent = data.get('urgent', False)
    ticket_id = data.get('ticketId')
    if not (thread_id and text):
        return jsonify({"error": "Thread ID and text are required"}), 400
    credentials = google.oauth2.credentials.Credentials(
        token=request.headers['Authorization']
    )
    message_id = generate_message_id()
    messages[message_id] = {'threadId': thread_id, 'text': text, 'urgent': urgent, 'ticketId': ticket_id}
    return jsonify({"message": "Message sent successfully", "messageId": message_id}), 201

@app.route('/messages/<message_id>', methods=['GET'])
def get_message(message_id):
    message = messages.get(message_id)
    if message:
        return jsonify(message), 200
    else:
        return jsonify({"error": "Message not found"}), 404

def generate_message_id():
    return str(len(messages) + 1)

if __name__ == '__main__':
    app.run(debug=True)
