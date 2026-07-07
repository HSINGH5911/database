class Parser:

    def parse(self, data):
        lines = data.split("\r\n")

        command = []

        for line in lines:
            if not line:
                continue

            if line.startsWith("*"):
                continue

            if line.startsWith("$"):
                continue

            command.append(line)