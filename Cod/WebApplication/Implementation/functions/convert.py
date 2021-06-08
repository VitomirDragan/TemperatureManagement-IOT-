# Function that converts string to boolean
def toBoolean(admin_role):
    if admin_role == 'True':
        return True
    else:
        return False


# Function that converts string '1' or '0' to int
def toInt(switchIntervalsOn):
    if switchIntervalsOn == '1':
        return 1
    else:
        return 0
