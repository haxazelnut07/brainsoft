from flask import Flask, request, jsonify

app = Flask(__name__)

# Database sementara untuk menyimpan pesan terenkripsi
messages = []

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    messages.append(data)
    return jsonify({"status": "success", "message": "Pesan terkirim!"})

@app.route('/receive/<recipient>', methods=['GET'])
def receive_messages(recipient):
    user_messages = [msg for msg in messages if msg["recipient"] == recipient]
    return jsonify(user_messages)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

@app.route('/')
def home():
    return jsonify({"messages": messages})
