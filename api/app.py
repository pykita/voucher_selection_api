from flask import Flask, request, jsonify
from models.customer import Customer
from logger import logger
from storage import get_voucher_amount

app = Flask(__name__)


@app.route('/health')
def health():
    return 'OK'

@app.route('/segment/amount', methods=['GET'])
def get_segment_amount():
    obj = request.get_json()
    try:
        customer = Customer(**obj)
        segment_range = customer.find_segment()

        amount = get_voucher_amount(customer.segment_name, segment_range)
        return jsonify({'vocher_amount': amount})
    except Exception as e:
        logger.error('Something went wrong')
        logger.error(e)
    
    return 'Bad'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    