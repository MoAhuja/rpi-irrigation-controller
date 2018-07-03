from flask import jsonify

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, status_code=None,  field=None, error_message="Unkown Error", payload=None, ):
        Exception.__init__(self)
        self.error_message = error_message
        if status_code is not None:
            self.status_code = status_code
        
        self.payload = payload
        self.field=field

    def to_dict(self):
        rv = {}
        payload = dict(self.payload or ())
        rv['request'] = payload
        rv['error'] = self.error_message
        rv['field'] = self.field
        return rv