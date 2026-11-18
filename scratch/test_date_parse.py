from datetime import datetime
import zoneinfo

IST = zoneinfo.ZoneInfo('Asia/Kolkata')
ts1 = '05 Nov 2026, 10:32 PM IST'
dt1 = datetime.strptime(ts1, '%d %b %Y, %I:%M %p IST').replace(tzinfo=IST)
print('Parsed ts1:', dt1, 'Date:', dt1.date().isoformat())

ts2 = '2026-11-16T10:15:30+05:30'
dt2 = datetime.fromisoformat(ts2).astimezone(IST)
print('Parsed ts2:', dt2, 'Date:', dt2.date().isoformat())
