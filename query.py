import sqlite3
import pandas as pd
from datetime import datetime

parentFolder = r"C:\Users\Vinayak Nishant\Desktop\Projects\Zing_Intern_Task"
DRIVER_PATH = r"C:\Users\Vinayak Nishant\Desktop\Drivers\chromedriver.exe"

with open('latest.txt') as f:
    latest_file = f.read()

latest_date = datetime.strptime(latest_file[2:11],"%d%b%Y")
print(latest_date)

latest_date = "2022-11-15 00:00:00"

# Queries
file = r"C:\Users\Vinayak Nishant\Desktop\Projects\Zing_Intern_Task\database\sqlite3.db"
conn = sqlite3.connect(file)

cur = conn.cursor()

# Question 1 Solution
query_one = f''' SELECT * FROM equity AS e
INNER JOIN bhavcopy AS b 
ON e.SYMBOL = b.SYMBOL
WHERE b.DATE = "{latest_date}"
ORDER BY b.GAIN DESC
LIMIT 25;'''

data = cur.execute(query_one)
for row in data:
    print(row)


# Question 2 Solution
query_second = ''' 
SELECT SYMBOL, GAIN,DATE FROM (
    SELECT *, row_number() OVER 
    ( PARTITION BY DATE ORDER BY GAIN DESC ) AS gain_rank
    FROM (
        SELECT * FROM equity AS e
        INNER JOIN bhavcopy AS b 
        ON e.SYMBOL = b.SYMBOL
    )
) 
WHERE gain_rank <= 2
ORDER BY DATE, GAIN DESC 
'''

data = cur.execute(query_second)
for row in data:
    print(row)



# Question 3 Solution
df = pd.read_csv("bhavcopy.csv")
symbols = df["SYMBOL"].unique()
gainers = []

for symbol in symbols:
    # print(symbol)
    min_date = min(df[df["SYMBOL"]== symbol]["DATE"].values)
    max_date = max(df[df["SYMBOL"]== symbol]["DATE"].values)

    # print(min_date, max_date)

    open = df[df["SYMBOL"]== symbol][df["DATE"] == min_date]["OPEN"].values[0]
    close = df[df["SYMBOL"]== symbol][df["DATE"] == max_date]["CLOSE"].values[0]

    # print(open,close)
    
    gain = ((close-open)/close)

    gainer = pd.DataFrame([[symbol,open,close,gain]],columns = ["SYMBOL","OPEN","CLOSE","GAIN"])
    gainers.append(gainer)


bhavcopy = pd.concat(gainers)
bhavcopy.to_sql('new_bhavcopy', conn, if_exists = 'replace', index = False)

cur = conn.cursor()

query_third = '''
SELECT * FROM equity AS e
INNER JOIN new_bhavcopy AS b 
ON e.SYMBOL = b.SYMBOL
ORDER BY b.GAIN DESC
LIMIT 25;
'''
data = cur.execute(query_third)
for row in data:
    print(row)
