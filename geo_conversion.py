import argparse
import re  # regular expressions

# TODO: customizable formats


def prepareString(input_string: str) -> list:
    # unify string
    s = input_string.upper()
    s = s.replace(' ', '')
    s = s.replace('°', '')
    s = s.replace('+', '')

    # split coordinates
    regex = "([-]?\d+[.,]?\d*[NS]?),([-]?\d+[.,]?\d*[EW]?)"
    parts = re.findall(regex, s)
    if (len(parts) != 1):  # any match found?
        print("Error: Invalid input.")
        return [0, 0]
    parts = parts[0]
    if (len(parts) != 2):  # only two parts (long- and latitude)?
        print("Error: Invalid input.")
        return [0, 0]
    parts = list(parts)

    # convert string to float
    for i in range(2):
        parts[i] = parts[i].replace(',', '.')
        parts[i] = parts[i].replace('N', '')
        parts[i] = parts[i].replace('E', '')
        # South or West -> negative float
        if (parts[i].find('S') != -1 or parts[i].find('W') != -1):
            parts[i] = parts[i].replace('S', '')
            parts[i] = parts[i].replace('W', '')
            parts[i] = "-" + parts[i]
        parts[i] = float(parts[i])
    return parts


def degrees(decimal_degrees: list) -> list:
    # latitude
    latitude = ""
    if (decimal_degrees[0] < 0):  # south
        latitude = conv(decimal_degrees[0], 'S')
    else:
        latitude = conv(decimal_degrees[0], 'N')

    # longitude
    longitude = ""
    if (decimal_degrees[1] < 0):  # south
        longitude = conv(decimal_degrees[1], 'W')
    else:
        longitude = conv(decimal_degrees[1], 'E')

    return [latitude, longitude]


def conv(decimal: float, direction_char: str) -> str:
    decimal = abs(decimal)
    degree = int(decimal)
    minutes = (decimal - degree) * 60
    seconds = (minutes - int(minutes)) * 60
    s = f"{degree:02d}" + "° " + \
        f"{int(minutes):02d}" + "' " + \
        f"{seconds:.2f}".zfill(5) + '\"' + direction_char
    return s


def perform_tests():
    f = open("testfile.txt", "r")
    lines = f.readlines()
    for line in lines:
        line = line.replace("\n", "")
        res = degrees(prepareString(line))
        print(res[0] + ", " + res[1])
    f.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input string")
    args = parser.parse_args()

    # conversion
    res = degrees(prepareString(args.input))
    print(res[0] + ", " + res[1])


if __name__ == "__main__":
    main()
