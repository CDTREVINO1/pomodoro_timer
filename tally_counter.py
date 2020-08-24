import time
import datetime
import subprocess
from datetime import timedelta


def convert_tallies_and_times(contents):
    """Convert string to a dates and tallies dictionary, return the dict"""
    date_contents = contents.split('\n')

    # Place the dates into a dictionary as keys and tallies as values
    dates_tallies = {}
    for string in date_contents:
        dates, tallies = string.split(':')
        dates_tallies[dates] = tallies
    return dates_tallies


def count_all_tallies_and_times(contents):
    """Count the total tallies and minutes of all time and return them."""
    dates_tallies = convert_tallies_and_times(contents)
    total_tallies = []
    for dates, tallies in dates_tallies.items():
        tallies = tallies.split(' ')
        for tally in tallies:
            if tally == '':
                continue
            else:
                total_tallies.append(int(tally))
    return total_tallies


def count_day_tallies_and_times(date, contents):
    """Count the tallies and times for any given date"""
    dates_tallies = convert_tallies_and_times(contents)
    if date in contents:
        day_tallies = dates_tallies[date]
        day_minutes = list(day_tallies.split(' '))
        day_minutes = list(filter(None, day_minutes))
        day_minutes = list(map(int, day_minutes))
        day_tallies = len(day_minutes)
        day_minutes = sum(day_minutes)
        return day_tallies, day_minutes


today = datetime.date.today()
yesterday = (today - timedelta(days=1))

numdays = 7
date_list = [today - datetime.timedelta(days=x) for x in range(numdays)]

# Open log file and append the current date or tally a pomodoro.
with open('pomodoro_tracker.txt', 'r') as file_object:
    contents = file_object.read()

    # Pomodoro and time count for all time
    count_all_tallies_and_times(contents)

    # Pomodoro and time count for today
    today = today.isoformat()
    if today in contents:
        t_tallies, t_minutes = count_day_tallies_and_times(today, contents)
        print(
            'Total pomodoros today:', t_tallies, ', for a total of', t_minutes,
            'minutes', 'or', t_minutes // 60, 'hours.'
        )
    else:
        print('No pomodoros done yet today.')

    # Pomodoro and time count for yesterday
    yesterday = yesterday.isoformat()
    if yesterday in contents:
        y_tallies, y_minutes = count_day_tallies_and_times(yesterday, contents)
        print(
            'Total pomodoros yesterday:', y_tallies, ', for a total of',
            y_minutes, 'minutes', 'or', y_minutes // 60, 'hours.'
        )
    else:
        print("Total pomodoros yesterday: 0")

    # All time pomodoro and time count
    total_tallies = count_all_tallies_and_times(contents)
    print(
        'Total pomodoros to date:', len(total_tallies), 'for a total time of',
        sum(total_tallies), 'minutes or', sum(total_tallies) // 60, 'hours.'
    )

# At the end of the countdown, open a text file.
# subprocess.Popen(['open', 'pomodoro_tracker.txt'])
