class Serializer:

    @staticmethod
    def simple_string(value):
        return f"+{value}\r\n"

    @staticmethod
    def error(message):
        return f"-ERR {message}\r\n"

    @staticmethod
    def integer(value):
        return f":{value}\r\n"

    @staticmethod
    def bulk_string(value):
        if value is None:
            return "$-1\r\n"
        val_str = str(value)
        return f"${len(val_str)}\r\n{val_str}\r\n"

    @staticmethod
    def array(items):
        if items is None:
            return "*-1\r\n"
        if not isinstance(items, list):
            items = list(items)
        
        result = [f"*{len(items)}\r\n"]
        for item in items:
            result.append(Serializer.serialize(item))
        return "".join(result)

    @staticmethod
    def serialize(value):
        if value is None:
            return Serializer.bulk_string(None)
        if isinstance(value, bool):
            return Serializer.integer(1 if value else 0)
        if isinstance(value, int):
            return Serializer.integer(value)
        if isinstance(value, str):
            if value.startswith("ERR") or value.startswith("WRONGTYPE"):
                return Serializer.error(value)
            if value == "OK" or value == "PONG":
                return Serializer.simple_string(value)
            return Serializer.bulk_string(value)
        if isinstance(value, (list, set, tuple)):
            return Serializer.array(list(value))
        return Serializer.bulk_string(str(value))