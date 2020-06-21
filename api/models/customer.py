from pydantic import BaseModel, ValidationError, validator, PositiveInt
from datetime import datetime
# from .segments import segments



class Customer(BaseModel):
    customer_id: int
    country_code: str
    first_order_ts: datetime
    last_order_ts: datetime
    total_orders: PositiveInt
    segment_name: str

    _segments = {
        'frequency_segment': {
            '0-4': lambda i: i >= 0 and i <= 4,
            '5-13': lambda i: i >= 5 and i <= 13,
            '14-37': lambda i: i >= 14 and i <= 37,
            '38+': lambda i: i >= 38
        },
        'recency_segment': {
            '0-30': lambda i: i >= 0 and i <= 30, 
            '31-60': lambda i: i >= 31 and i <= 60, 
            '61-90': lambda i: i >= 61 and i <= 90, 
            '91-120': lambda i: i >= 91 and i <= 120, 
            '121-180': lambda i: i >= 121 and i <= 180, 
            '181+': lambda i: i >= 181
        }
    }

    def find_segment(self):
        if self.segment_name == 'frequency_segment':
            segment_value = self.total_orders
        elif self.segment_name == 'recency_segment':
            segment_value = (last_order_ts - first_order_ts).days

        for key, condition in self._segments[self.segment_name].items():
            if condition(segment_value):
                return key
        
        raise Exception('Value is out of bounds')

    @validator('country_code')
    def only_peru(cls, value):
        if 'Peru' != value:
            raise ValueError('only Peru countries')
        return value

    @validator('last_order_ts')
    def last_more_or_equal_than_first(cls, value, values):
        if values['first_order_ts'] >= value:
            raise ValueError('last order cannot be earlier than first order')
        return value

    #maybe add if first == last then total_orders must be 1

    @validator('segment_name')
    def only_specific_segment_name(cls, value):
        if value not in cls._segments.keys():
            raise ValueError(f'only {" or ".join(segments.keys())} segment types')
        return value
