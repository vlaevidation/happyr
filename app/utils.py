def normalize_number(number):
    """Normalize a phone number str to format 18051234567"""
    number = number.replace('(', '')
    number = number.replace(')', '')
    number = number.replace('-', '')
    number = number.replace(' ', '')
    number = number.replace('.', '')
    if len(number) < 12:
        number = "+1{}".format(number)
    return number
