import pandas as pd
import datetime as dt
df = pd.DataFrame(columns=["year", "month", "day", "hour", "minute", "second"])
now = dt.datetime.now()
df.loc[len(df)] = [now.year, now.month, now.day, now.hour, now.minute, now.second]
df.to_csv("filename.csv", index=False)
print(df)
