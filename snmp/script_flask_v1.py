from flask import Flask, request, jsonify
from script_snmp import main, verify_and_select

app = Flask(__name__)

@app.route('/script', methods=['POST'])
def web_app():
    key = "key12345"
    api_key =request.headers.get("X-API-Key")
    if api_key != key:
        return jsonify({"error": "Unauthorized"}), 401
    request_data = request.get_json() or {}
    ip = request_data['ip']
    serial = request_data['sn']
    result_dict = main(ip) 
    reply_data = verify_and_select(result_dict, serial)
    return jsonify(reply_data), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
