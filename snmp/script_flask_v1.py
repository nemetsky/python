from flask import Flask, request, jsonify
from script_snmp import main, verify_sn_and_select, check_dns
from werkzeug.middleware.proxy_fix import ProxyFix     # для определения клиента
import logging

root_logger = logging.getLogger()
root_logger.setLevel("DEBUG")
file_handler = logging.FileHandler("snmp.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s | %(levelname)8s | %(name)13s | %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )
)
root_logger.addHandler(file_handler)
logger = logging.getLogger("module_flask")
logger.setLevel("INFO")

app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)    # для определения IP клиента

@app.route('/script', methods=['POST'])
def web_app():
    key = "key12345"
    client_ip = request.remote_addr
    api_key = request.headers.get("X-API-Key")
    if api_key != key:
        logger.error("-> Получен неверный API ключ")
        return jsonify({"error": "Unauthorized"}), 401
    request_data = request.get_json() or {}
    ip = request_data['ip']
    hostname = request_data['name']
    serial = request_data['sn']
    logger.info(f"-> Получен запрос по HTTPS от {client_ip}: (опросить устройство: {ip}, hostname: {hostname}, SN: {serial})")
    dns_check_output = check_dns(ip, hostname)
    if isinstance(dns_check_output, str):
        return jsonify(dns_check_output), 200 
    result = main(ip)
    if isinstance(result, dict):
        reply_data = verify_sn_and_select(result, serial)
        if isinstance(reply_data, list):
            logger.info(f"<- Результат опроса {ip} успешно отправлен клиенту")
        else:
            logger.error(f"<- Результат опроса {ip} отправлен клиенту с ошибкой")
        return jsonify(reply_data), 200
    else:
        logger.error(f"<- Результат опроса {ip} отправлен клиенту с ошибкой")
        return jsonify(result), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
