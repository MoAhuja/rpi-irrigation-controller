from flask import jsonify

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, status_code=None,  field=None, error_message="Unknown Error", payload=None, invalid_field_value=None ):
        Exception.__init__(self)
        self.error_message = error_message
        if status_code is not None:
            self.status_code = status_code
        
        self.payload = payload
        self.field=field
        self.invalid_field_value = invalid_field_value

    def to_dict(self):
        rv = {}
        if self.payload is not None:
            payload = dict(self.payload or ())
            rv['request'] = payload
        
        if self.error_message is not None:
            rv['error'] = self.error_message
        
        if self.field is not None:
            rv['field'] = self.field

        if self.invalid_field_value is not None:
            rv['invalid_value'] = self.invalid_field_value
        return rv