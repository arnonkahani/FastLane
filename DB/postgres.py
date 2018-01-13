import psycopg2
from postgis.psycopg import register
from time import time
try:
    conn = psycopg2.connect("dbname='fastlanes3' user='postgres' host='localhost' password='k1k2k3d4'")
    register(conn)
    cur = conn.cursor()


    time_S = time()
    print("start: " + str(time_S))

    cur.execute("""SELECT * from public.stops""")
    rows = cur.fetchall()
    time_S = time() - time_S

    print("end: " + str(time_S))
    print(len(rows))
    print("\nShow me the databases:\n")
    for row in rows:
        print("   ", row[1][1])
except:
    print("I am unable to connect to the database")