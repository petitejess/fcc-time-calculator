def is_valid_duration(duration_str):
  if (isinstance(duration_str, str)):
    [hours, minutes] = duration_str.split(":")

    if (hours.isdigit() and (minutes.isdigit() and 0 <= int(minutes) <= 60)):
      return {"status": True, "message": "Good."}

  return {
    "status":
    False,
    "message":
    "Error: Invalid duration. Please enter input in hour:minute format."
  }


def format_str_24_hour(time_string, day_of_week):
  start_hours = time_string.split(":")[0]
  [start_minutes, am_pm] = time_string.split(":")[1].split(" ")
  return {
    "hours":
    (int(start_hours) + 12) if am_pm.lower() == 'pm' else int(start_hours),
    "minutes":
    int(start_minutes),
    "day":
    day_of_week.lower() if day_of_week else ""
  }


def format_time_12_hour(hours, minutes, days, day_of_week):
  day_names = {
    "monday": 1,
    "tuesday": 2,
    "wednesday": 3,
    "thursday": 4,
    "friday": 5,
    "saturday": 6,
    "sunday": 7
  }

  am_pm = "PM" if hours > 11 else "AM"
  hour_12 = hours - 12 if hours > 12 else hours
  day_number = (day_names[day_of_week.lower()] + days) if day_of_week else 0
  the_day = ""
  day_number_str = ""

  if (day_number):
    # Get the name of the day
    for d_name, d_key in day_names.items():
      if d_key == (day_number % 7 if day_number > 7 else day_number):
        the_day = d_name.capitalize()

  if (days):
    # Get the number of the day
    if (days == 1):
      day_number_str = " (next day)"
    else:
      day_number_str = f" ({days} days later)"

  time_string = f"{12 if (hour_12 == 0 and am_pm == 'AM') else hour_12}:{minutes if minutes > 9 else ('0' + str(minutes))} {am_pm}{', ' + the_day if day_of_week else ''}{day_number_str}"

  return time_string


def add_time(start, duration, day_of_week=None):
  if (is_valid_duration(duration)["status"]):
    start_in_24_format = format_str_24_hour(start, day_of_week)

    [add_hours, add_minutes] = duration.split(":")

    day_calculation = 0
    hour_calculation = start_in_24_format["hours"] + int(add_hours)
    minute_calculation = start_in_24_format["minutes"] + int(add_minutes)

    if (minute_calculation > 59):
      excess_hours = minute_calculation // 60
      hour_calculation += excess_hours
      minute_calculation -= (excess_hours * 60)

    if (hour_calculation > 23):
      excess_days = hour_calculation // 24
      day_calculation += excess_days
      hour_calculation -= (excess_days * 24)

  new_time = format_time_12_hour(hour_calculation, minute_calculation,
                                 day_calculation, day_of_week)

  return new_time


print(add_time("3:00 PM", "3:10"))
# Returns: 6:10 PM

print(add_time("11:30 AM", "2:32", "Monday"))
# Returns: 2:02 PM, Monday

print(add_time("11:43 AM", "00:20"))
# Returns: 12:03 PM

print(add_time("10:10 PM", "3:30"))
# Returns: 1:40 AM (next day)

print(add_time("11:43 PM", "24:20", "tueSday"))
# Returns: 12:03 AM, Thursday (2 days later)

print(add_time("6:30 PM", "205:12"))
# Returns: 7:42 AM (9 days later)
