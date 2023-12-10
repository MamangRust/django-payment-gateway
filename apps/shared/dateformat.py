from datetime import datetime


def date_format(date):
    formatted_date = datetime.strftime(date, "%d %B %Y, %H:%M:%S")
    return formatted_date
