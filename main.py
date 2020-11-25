import json
import datetime
from datetime import date
import psycopg2
import sys

today = date.today()

# Reading data
content = ""
try:
    f = open("data.json", "r")
    content = f.read()
except Exception:
    print("File read error!")
    sys.exit()

# Opening DB connection
con = None
try:
    con = psycopg2.connect(database="postgres", user="postgres", password="password", host="127.0.0.1", port="5432")
    print("Database opened successfully!")
except Exception:
    print("Database connection error")
    sys.exit()

d = json.loads(content)

# iterating over subscriptions
for key in d.keys():
    sub_array = d[key]
    trial_flag = False
    trial = 0
    paid = 0
    for i in range(len(sub_array)):
        t = sub_array[i]
        if t['is_trial_period'] == "true":
            trial_start_dt = t['purchase_date'].split()[0]
            trial += 1
            trial_flag = True
        else:
            paid += 1
            if trial_flag:
                subs_start_dt = t['purchase_date'].split()[0]
                trial_flag = False

        if i == (len(sub_array) - 1):
            exp_dt = t['expires_date'].split()[0]

    expiration_date = datetime.datetime.strptime(exp_dt, "%Y-%m-%d").date()
    status = ""
    if paid != 0:
        if expiration_date > today:
            status = "Active Subscription"
        else:
            status = "Expired Subscription"
    else:
        if expiration_date > today:
            status = "Active Trial"
        else:
            status = "Expired Trial"

    cur = con.cursor()
    id = key[::-1][0]
    sql = "INSERT INTO itunes_subscription (Id,transactions, trial_start_date, subscription_start_date, Expiration_date, current_status) VALUES (%s, %s,%s, %s, %s, %s)";
    cur.execute(sql, (id, json.dumps(sub_array), trial_start_dt, subs_start_dt, exp_dt, status));
    con.commit()

print("Records inserted successfully")
con.close()
