from datetime import datetime, date
import pytz


def toBoolean(admin_role):
    if admin_role == 'True':
        return True
    else:
        return False


def toInt(switchIntervalsOn):
    if switchIntervalsOn == '1':
        return 1
    else:
        return 0


def getHourFromTimeFormat(timeFormat):
    tokens = timeFormat.split(':')
    return int(tokens[0])


def getMinuteFromTimeFormat(timeFormat):
    tokens = timeFormat.split(':')
    return int(tokens[1])


def getTime(timeFormat):
    hour = getHourFromTimeFormat(timeFormat)
    minute = getMinuteFromTimeFormat(timeFormat)

    now = datetime.now(pytz.timezone('Europe/Bucharest'))
    dateTimeObject = datetime(now.year, now.month, now.day, hour, minute)

    return dateTimeObject
