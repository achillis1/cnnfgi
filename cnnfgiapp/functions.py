from datetime import datetime, timedelta, date


def get_date(str):
    year, month, day = str.split('-')
    return date(int(year), int(month), int(day))
    

