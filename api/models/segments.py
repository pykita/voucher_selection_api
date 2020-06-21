segments = {
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

def find_segment(value, segment_type):
    for key, condition in segments[segment_type].items():
        if condition(value):
            return key
        else:
            raise Exception('Value is out of bounds')
