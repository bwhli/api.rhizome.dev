import os


def hex_to_int(input):
    return int(input, 16)


def human_format(num):
    num = float("{:.3g}".format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return "{}{}".format(
        "{:f}".format(num).rstrip("0").rstrip("."), ["", "K", "M", "B", "T"][magnitude]
    )


def is_production():
    if os.getenv("ENV") == "PRODUCTION":
        return True
    else:
        return False
