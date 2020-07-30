# pomodoro_timer.py - My own custom pomodoro timer with tracker log.

import time, datetime, subprocess, sys
from datetime import timedelta

# Get input for pomodoro duration, only accepts 25 - 60 mins for each.
while True:
    time_left = input("Type a number 25 - 60 for your desired pomodoro "
                      "duration:"
                      "\nOr press ENTER to quit. "
                     )

    if time_left == '':
        sys.exit(0)

    if int(time_left) not in range(25, 61):
        continue

    if int(time_left) in range(25, 61):
        time_left = int(time_left)
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
            file_object.write(' 1')
        else:
            file_object.write('\n' + today + ': 1')

        date_contents = contents.split('\n')
        
        dates_tallies = {}
        for string in date_contents:
            dates, tallies = string.split(':')
            dates_tallies[dates] = tallies

            total = 0
            for dates, tallies in dates_tallies.items():
                total += len(tallies.replace(' ', ''))

    if today in contents:
        today_tallies = dates_tallies[today]
        today_tallies = len(today_tallies.replace(' ', ''))
        print('Total pomodoros today: ' + str(today_tallies + 1))
    else:
        print('Total pomodoros today: 1')

    if yesterday in contents:
        yesterday_tallies = dates_tallies[yesterday]
        yesterday_tallies = len(yesterday_tallies.replace(' ', ''))
        print('Total pomodoros yesterday: ' + str(yesterday_tallies))
    else:
        print("Total pomodoros yesterday: 0")

    print('Total pomodoros to date: ' + str(total))
    
    # At the end of the countdown, open a text file.
    subprocess.Popen(['open', 'pomodoro_tracker.txt'])
except KeyboardInterrupt:
    print('\nCancelled.\n')