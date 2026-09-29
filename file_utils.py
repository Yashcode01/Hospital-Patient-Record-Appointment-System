def read_lines(filename):
    try:
        file = open(filename, "r")
        lines = file.readlines()
        file.close()
        cleaned = []
        for line in lines:
            line = line.strip()
            if line != "":
                cleaned.append(line)
        return cleaned
    except FileNotFoundError:
        return []


def write_lines(filename, lines):
    try:
        file = open(filename, "w")
        for line in lines:
            file.write(line + "\n")
        file.close()
        return True
    except IOError as error:
        print(f"Could not save to {filename}: {error}")
        return False
