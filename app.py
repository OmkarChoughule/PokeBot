from flask import Flask, request, jsonify
from Chatbot import handle_query  

app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message", "")
    response = handle_query(user_message)
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(debug=True, port=5500)
