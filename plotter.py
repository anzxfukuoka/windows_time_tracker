import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from config import data_file

# raw data
data = pd.read_csv(data_file, index_col = False)

data["date_time"] = pd.to_datetime(data["date_time"])
print(data.head())

# relative time

spend_time = []

for row in range(len(data) - 1):
    spend_time.append(data.iloc[row + 1].loc["date_time"] - data.iloc[row].loc["date_time"])

spend_time.append(data.iloc[len(data) - 1 ].loc["date_time"] - data.iloc[len(data)  - 1].loc["date_time"])

rel_data = data.copy()

rel_data["spend_time"] = spend_time
rel_data = rel_data.groupby("app_name").sum()

rel_data["spend_time"] = rel_data["spend_time"].astype('timedelta64[s]')

print(rel_data)

# plot

# шаблон отображения процентного значения
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct

rel_data.plot.pie(
    #labels=data["app_name"],
    #colors=["c", "m", "b", "g"],
    autopct=make_autopct(rel_data["spend_time"]), #"%.2f",
    fontsize=12,
    figsize=(6, 6),
    y='spend_time',
    ylabel="Total seconds")
plt.show()
