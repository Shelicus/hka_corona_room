import sqlite3


def anzeigen(ID):
    try:
        conn = sqlite3.connect('Path')
        c = conn.cursor()
        with conn:
            c.execute("SELECT * FROM speicher_zustand WHERE id=:id", {'id': ID})
            daten = c.fetchall()
        conn.commit()
        conn.close()
        return daten
    except Exception as fehler11:
        print('Fehler 11: \n')
        print(fehler11)
        return -1

def alles_anzeigen():
    try:
        conn2 = sqlite3.connect('Path')
        d = conn2.cursor()
        with conn2:
            d.execute("SELECT * FROM speicher_zustand")
            daten = d.fetchall()
        conn2.commit()
        conn2.close()
        return daten
    except Exception as fehler15:
        print('Fehler 15: \n')
        print(fehler15)
        return -1

def hinzufuegen(Fach, ID, UhrzeitTag, Raum):
    try:
        conn = sqlite3.connect('Path')
        c = conn.cursor()
        with conn:
            c.execute("INSERT INTO speicher_zustand VALUES (:fach, :id, :uhrzeittag, :raum)",
                      {'fach': Fach, 'id': ID, 'uhrzeittag': UhrzeitTag, 'raum': Raum})
        conn.commit()
        conn.close()
        return 1
    except Exception as fehler12:
        print('Fehler 12: \n')
        print(fehler12)
        return -1


def update_datenbank(Fach, ID, UhrzeitTag, Raum):
    try:
        conn = sqlite3.connect('Path')
        c = conn.cursor()
        with conn:
            c.execute("""UPDATE speicher_zustand SET fach = :fach, raum = :raum, uhrzeittag = :uhrzeittag
                        WHERE id = :id""", {'fach': Fach, 'id': ID, 'uhrzeittag': UhrzeitTag, 'raum': Raum})
        conn.commit()
        conn.close()
        return 1
    except Exception as fehler13:
        print('Fehler 13: \n')
        print(fehler13)
        return -1


def delete_liste():
    try:
        conn = sqlite3.connect('Path')
        c = conn.cursor()
        with conn:
            c.execute("DELETE FROM speicher_zustand")
        conn.commit()
        conn.close()
        return 1
    except Exception as fehler14:
        print('Fehler 14: \n')
        print(fehler14)
        return -1