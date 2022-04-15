def time_formatter(time, timezone="ET"):
    """
    This function takes times only in the format ISO 8601 format (2022-04-08T23:00:00Z) and converts them to a readable time.
    The function does not return minuites if they are '00'. The return includes AM/PM and the timezone.
    Users may choose from ET, CT, MT, PT, or AKT timezones. ET is set as the default.    
    """
    # @Jack, we can set this up where a user selects their perferred timezone when they sign up for the service.

    # dictionary to convert timezone abbreviations to the needed inputs for pytz
    abbreviations = {'ET':'America/New_York','CT':'America/North_Dakota/Center','MT':'America/Denver','PT':'America/Los_Angeles','AKT':'America/Juneau'}

    # utc to ET time conversion syntax from xster, a medium user: 
    # https://medium.com/xster-tech/python-convert-iso8601-utc-to-local-time-a386652b0306
    import pytz, dateutil.parser
    utc_time = dateutil.parser.parse(time)
    local_time = utc_time.astimezone(pytz.timezone(abbreviations[timezone]))

    local_time = str(local_time)
    hour = int(local_time[11:][:2])
    minutes = int(local_time[14:][:2])

    if minutes == 0:
        if hour > 12:
            return (str(hour - 12) + 'PM' + ' ' + timezone)
        else:
            return (str(hour) + 'AM' + ' ' + timezone)
    else:
        if hour > 12:
            return (str(hour - 12) + ':' + str(minutes) + 'PM' + ' ' + timezone)
        else:
            return (str(hour) + ':' + str(minutes) + 'AM' + ' ' + timezone) 
