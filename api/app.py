from flask import Flask, request, jsonify
from models.customer import Customer
from logger import logger
from storage import get_voucher_amount
from datetime import datetime

app = Flask(__name__)


@app.route('/health')
def health():
    return 'OK'

@app.route('/segment/amount', methods=['GET'])
def get_segment_amount():
    obj = request.get_json()
    obj['now_ts'] = datetime(2018, 8, 5) # in order to have more beautiful results we setup datetime.utcnow()
    try:
        # create and validate request
        customer = Customer(**obj)

        #find a proper segment
        segment_range = customer.find_segment()

        # get amount for a specific segment
        amount = get_voucher_amount(customer.segment_name, segment_range)

        return jsonify({'vocher_amount': amount})
    except Exception as e:
        logger.error('Something went wrong')
        logger.error(e)
        # Return error
        return 'Something went wrong'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    