import os
import sqlite3
import pandas as pd
from datetime import datetime
# from download import latest_file

parentFolder = r"C:\Users\Vinayak Nishant\Desktop\Projects\Zing_Intern_Task"
DRIVER_PATH = r"C:\Users\Vinayak Nishant\Desktop\Drivers\chromedriver.exe"


# Generating SQL Database for CSV
file = r"C:\Users\Vinayak Nishant\Desktop\Projects\Zing_Intern_Task\database\sqlite3.db"
conn = sqlite3.connect(file)

# Equity Table
equity = pd.read_csv("EQUITY_L.csv")
equity.to_sql('equity', conn, if_exists = 'replace', index = False)


# Bhavcopy Table with date
files = os.listdir(parentFolder + r"\bhavcopy")
dfs = []

for file in files:
    # print(file)
    df = pd.read_csv(parentFolder + r"\bhavcopy\\" + file, index_col = False)
    df["GAIN"] = df.apply(lambda row: (row.CLOSE - row.OPEN)/row.OPEN, axis = 1)
    df["DATE"] = datetime.strptime(file[2:11],"%d%b%Y")
    dfs.append(df)

bhavcopy = pd.concat(dfs, ignore_index=True)
bhavcopy.to_csv("bhavcopy.csv", index = False)

print(bhavcopy.head())
print(bhavcopy.shape)

bhavcopy.to_sql('bhavcopy', conn, if_exists = 'replace', index = False)
conn.close()