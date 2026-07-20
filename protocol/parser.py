class Parser:

    def parse(self, data):
        if not data:
            return []

        if isinstance(data, bytes):
            data = data.decode("utf-8", errors="replace")

        data = data.strip()
        if not data:
            return []

        # Handle RESP array (starts with '*')
        if data.startswith("*"):
            return self._parse_resp_array(data)

        # Handle RESP bulk string (starts with '$')
        if data.startswith("$"):
            res = self._parse_bulk_string(data)
            return [res] if res else []

        # Plain inline command (e.g. "SET key val")
        return data.split()

    def _parse_resp_array(self, data):
        lines = data.split("\r\n")
        if not lines or not lines[0].startswith("*"):
            return data.split()

        try:
            num_elements = int(lines[0][1:])
        except ValueError:
            return data.split()

        tokens = []
        i = 1
        while i < len(lines) and len(tokens) < num_elements:
            line = lines[i]
            if line.startswith("$"):
                if i + 1 < len(lines):
                    tokens.append(lines[i + 1])
                    i += 2
                else:
                    break
            elif line.startswith("+") or line.startswith(":") or line.startswith("-"):
                tokens.append(line[1:])
                i += 1
            else:
                if line:
                    tokens.append(line)
                i += 1

        return tokens

    def _parse_bulk_string(self, data):
        lines = data.split("\r\n")
        if len(lines) >= 2:
            return lines[1]
        return data.lstrip("$")