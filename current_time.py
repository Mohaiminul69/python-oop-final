from datetime import datetime


def current_time():
    date_str = f"{datetime.now()}"
    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
    formatted_date = date_obj.strftime("%d %b %Y, %I:%M %p")
    return formatted_date
