#!/usr/bin/env python3

import calendar
from datetime import datetime

today_time = datetime.now()
cal = calendar.Calendar()

print('''PopUp "CalendarPopup" {
  AutoClose = true
  style = "cal_pop_style"

  grid "CalendarPopupGrid" {
   style = "cal_pop_grid_style"
   label "caltime" {
      value = Time("%A            %H:%M %Z")
      style = 'header_time'
   }
   label "caldate" {
      value = Time("%B %d, %Y")
      style = "header_date"
   }
    ''')

sfw_cal = cal.monthdayscalendar(today_time.year, today_time.month)
#sfw_cal.insert(0, calendar.weekheader(2).split(' '))

header = '  grid {\n    style = "cal_line"\n'
for i in calendar.weekheader(2).split(' '):
    header += '      label {\n        value = "' + i + '"\n        style = "aday"\n    }\n'
print(header + '}')

for w in sfw_cal:
    week_line = '  grid {\n    style = "cal_line"\n'
    for d in w:
        week_line += '      label {\n        value = "'
        if d == 0:
            week_line += '  '
        elif d <= 9:
            #print("_{}_".format(d), end=' ')
            week_line += ' ' + str(d)
        else:
            week_line += str(d)

        week_line += '"\n'
        if d == today_time.day:
            week_line += '        style = "today"\n'
        else:
            week_line += '        style = "aday"\n'
            #print(d, end=' ')
        week_line += '      }\n'
    print(week_line + '  }')

print('  }\n}')
