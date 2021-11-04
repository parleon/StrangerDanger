import sqlite3
from datetime import datetime

con = sqlite3.connect('data.db')
cur = con.cursor()

try:
    cur.execute('''
            CREATE TABLE snapshot (
                SnapshotID integer PRIMARY KEY,
                Duration integer,
                Datetime datetime
            )
            ''')

    cur.execute('''
            CREATE TABLE device (
                DeviceID integer PRIMARY KEY,
                Address text UNIQUE NOT NULL,
                Name text,
                Metadata text,
                Dangerous integer
            )
            ''')

    cur.execute('''
            CREATE TABLE appearence (
                RSSI integer,
                sID integer, 
                dID integer, 
                FOREIGN KEY(sID) REFERENCES snapshot(SnapshotID),
                FOREIGN KEY(dID) REFERENCES device(DeviceID)
            )
            ''')

    con.commit()
    con.close()

    print("DB initialized")

except: 
    print("DB already initialized")

def add_snapshot(duration):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    con = sqlite3.connect('data.db')
    cur = con.cursor()
    cur.execute('''
                INSERT INTO snapshot (Duration, Datetime) VALUES (?, ?)
                ''', (duration, now))
    con.commit()
    con.close()

def add_device(address, name, metadata, dangerous=0):

    try:
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute('''
                    INSERT INTO Device (Address, Name, Metadata, Dangerous) VALUES (?, ?, ?, ?)
                    ''', (address, name, metadata, dangerous))
        con.commit()
        con.close()

        return 1 # device added
    except:
        try:
            con = sqlite3.connect('data.db')
            cur = con.cursor()
            cur.execute('''
                    UPDATE Device SET Name = ?, Metadata = ? WHERE Address = ?
                    ''', (name, metadata, address))
            con.commit()
            con.close()
            return 0 # device updated
        except:
            return -1 # device already exists

def make_appearence(address, rssi):
    con = sqlite3.connect('data.db')
    cur = con.cursor()

    cur.execute('''
                SELECT DeviceID FROM device WHERE Address = ?
                ''', (address,))
    dID = cur.fetchone()[0]

    cur.execute('''
                SELECT MAX(SnapshotID) FROM snapshot
                ''')
    sID = cur.fetchone()[0]

    cur.execute('''
                INSERT INTO appearence (RSSI, sID, dID) VALUES (?,?,?)
                ''', (rssi,sID,dID))

    con.commit()
    con.close()

def get_device(address):
    con = sqlite3.connect('data.db')
    cur = con.cursor()

    cur.execute('''
                SELECT 1 FROM device WHERE Address = ?
                ''', (address,))
    device = cur.fetchall()
    con.commit()
    con.close()

    if len(device) == 0:
        return False

    return device[0]
