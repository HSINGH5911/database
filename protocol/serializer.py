class Serializer:

    def simple_string(value):
        return f"+{value}\r\n"
    
    def integer(value):
        return f":{value}\r\n"
    
    def bulk_string(value):
        if value is None:
            return "$-1\r\n"
        
        return f"${len(value)}\r\n{value}\r\n"
    
    def error(message):
        return f"-ERR {message}\r\n"