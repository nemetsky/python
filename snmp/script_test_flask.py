# скрип ждет запрос
# http POST http://172.16.111.50:5000/script hostname="r1" ip='1.1.1.1'
# и возвращает словарь, где имя роутера заглавными буквами будет

from flask import Flask, request, jsonify

app = Flask(__name__)

def main(name, ip):
    new_name = name.capitalize()
    my_dict = {
        "name": new_name,
        "address": ip
    }
    return my_dict

@app.route('/script', methods=['POST'])
def web_app():
    data = request.get_json() or {}
    hostname = data.get('hostname', 'nonane')
    ip = data['ip']
    new_data = main(hostname, ip)
    result = {
        "status": "success",
        "output": new_data
    }
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
