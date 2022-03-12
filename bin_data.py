#! usr/bin/env python3
import main
import pandas as pd

import io

file = main.import_csv_file()
data = pd.read_csv(file)
# time_option = input("")
df = data.set_index("Status")
# df["Match time(UTC)"] = pd.to_datetime(data_with_date["Match time(UTC)"].datetime.strftime("$m-$d-$Y"))
df.drop(index=['Cancelled','System cancelled','Appealing','Paid'], inplace=True)
df['Match_time'] = pd.to_datetime(df['Match time(UTC)']).dt.date
df.drop(columns=["Order Number", "Advertisement Order Number", 'Fiat Type', 'Exchange rate', 'Payment Method',
                 'Counterparty', 'Match time(UTC)'], inplace=True)
df['Match_time'] = df['Match_time'].astype('str')
time_df = df[(df['Match_time'] > '2021-12-00') & (df['Match_time'] < '2021-12-32')]
print(time_df)

# df.loc[main.datetime.date(year=2021,month=12,day=1):main.datetime.date(year=2021,month=12,day=31)]
#
# print(df.to_string())
# for name, dtype in df.dtypes.iteritems():
#     print(name, dtype)