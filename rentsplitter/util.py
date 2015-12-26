import decimal

class RentsplitterError(Exception):
    def __init__(self, msg, *args):
        super(RentsplitterError, self).__init__(*args)
        self.msg = msg

    def __repr__(self):
        return self.msg

def decimal_truncate(dec, prec):
    return dec.quantize(decimal.Decimal('1e-{}'.format(prec)), decimal.ROUND_DOWN)

def decimal_make(value, prec):
    try:
        d = decimal.Decimal(value)
        return decimal_truncate(d, prec)
    except decimal.InvalidOperation:
        raise RentsplitterError('Invalid value')
