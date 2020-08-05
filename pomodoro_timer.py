# pomodoro_timer.py - My own custom pomodoro timer with tracker log.

import time, datetime, subprocess, sys
from datetime import timedelta

# Get input for pomodoro duration, only accepts 25 - 60 mins for each.
while True:
    time_left = input("Type a number 25 - 60 for your desired pomodoro "
                      "duration:\n"
                      "Or press ENTER to quit. "
                     )

    if time_left == '':
        sys.exit(0)

    if int(time_left) not in range(25, 61):
        continue

    if int(time_left) in range(25, 61):
        time_left = int(time_left)
        time_tally = str(time_left)
        time_left = time_left * 60
        break

print("\nPress Ctrl-C to quit anytime but pomodoro won't be counted.\n")
try:
    while time_left > 0:
        print(round(time_left / 60, 2))
        time.sleep(1)
        time_left = time_left - 1

    today = datetime.date.today().isoformat()
    yesterday = (datetime.date.today() - timedelta(days=1)).isoformat()

    # Open log file and append the current date or tally a pomodoro.
    with open('pomodoro_tracker.txt', 'r+') as file_object:
        contents = file_object.read()
        
        if today in contents:
            file_object.write(' ' + time_tally)
        else:
            file_object.write('\n' + today + ': ' + time_tally)

        date_contents = contents.split('\n')
        
        # Place the dates into a dictionary as keys and tallies as values
        dates_tallies = {}
        for string in date_contents:
            dates, tallies = string.split(':')
            dates_tallies[dates] = tallies

            # Count the total tallies and minutes of all time
            total_tallies = []
            for dates, tallies in dates_tallies.items():
                tallies = tallies.split(' ')
                for tally in tallies:
                    if tally == '':
                        continue
                    else:
                        total_tallies.append(int(tally))

    # Pomodoro and time count for today
    if today in contents:
        today_tallies = dates_tallies[today]
        today_minutes = list(today_tallies.split(' '))
        today_minutes = list(filter(None, today_minutes))
        today_minutes = list(map(int, today_minutes))
        today_tallies = len(today_minutes)
        today_minutes = sum(today_minutes)
        print(
            'Total pomodoros today: ' + str(today_tallies) +
            ', for a total of ' + str(today_minutes) + ' minutes.'
        )
    else:
        print('Total pomodoros today: 1, for ' + time_tally + ' minutes.')

    # Pomodoro and time count for yesterday
    if yesterday in contents:
        yesterday_tallies = dates_tallies[yesterday]
        yesterday_minutes = list(yesterday_tallies.split(' '))
        yesterday_minutes = list(filter(None, yesterday_minutes))
        yesterday_minutes = list(map(int, yesterday_minutes))
        yesterday_tallies = len(yesterday_minutes)
        yesterday_minutes = sum(yesterday_minutes)
        print(
            'Total pomodoros yesterday: ' + str(yesterday_tallies) + 
            ', for a total of ' + str(yesterday_minutes) + ' minutes.'
        )
    else:
        print("Total pomodoros yesterday: 0")

    # All time pomodoro and time count
    print(
        'Total pomodoros to date: ' + str(len(total_tallies)) + 
        ' for a total time of ' + str(sum(total_tallies)) + ' minutes or ' +
        str(round(sum(total_tallies) / 60, 2)) + ' hours.'
    )
    
    # At the end of the countdown, open a text file.
    subprocess.Popen(['open', 'pomodoro_tracker.txt'])
except KeyboardInterrupt:
    print('\nCancelled.\n')