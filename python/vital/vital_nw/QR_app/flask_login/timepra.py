import datetime

dt1 = datetime.datetime(year=2017, month=10, day=10, hour=15, minute=20)
dt2 = datetime.datetime(year=2017, month=10, day=10, hour=15, minute=30)


print(dt1-dt2)
print((dt1-dt2).total_seconds())

print(dt2-dt1)
print((dt2-dt1).total_seconds())