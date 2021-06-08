from datetime import datetime
import pytz


# Extract the hour from string with time format
def getHourFromTimeFormat(timeFormat):
    tokens = timeFormat.split(':')  # Use split to separate in two tokens the string
    return int(tokens[0])  # Return the first token


# Extract the minute from string with time format
def getMinuteFromTimeFormat(timeFormat):
    tokens = timeFormat.split(':')  # Use split to separate in two tokens the string
    return int(tokens[1])  # Return the second token


# Return date-time object that contains the hour and minute of timeFormat received as parameter
def getTime(timeFormat):
    hour = getHourFromTimeFormat(timeFormat)  # Extract hour from timeFormat
    minute = getMinuteFromTimeFormat(timeFormat)  # Extract minute from timeFormat

    now = datetime.now(pytz.timezone('Europe/Bucharest'))  # Read the current date and time
    dateTimeObject = datetime(now.year, now.month, now.day, hour, minute)  # Create the date-time object

    return dateTimeObject  # Return date-time object
