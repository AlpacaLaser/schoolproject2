from datetime import datetime, timedelta
from abc import ABC, abstractmethod

print("**** HotelArt ****")


class Szoba(ABC):
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam

    @abstractmethod
    def osszkoltseg(self, napok_szama):
        pass


class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(13000, szobaszam)

    def osszkoltseg(self, napok_szama):
        return self.ar * napok_szama


class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(26000, szobaszam)

    def osszkoltseg(self, napok_szama):
        return self.ar * napok_szama


class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def uj_szoba(self, szoba):
        self.szobak.append(szoba)

    def foglalas(self, szobaszam, datum, napok_szama):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                foglalas_datum = datetime.strptime(datum, "%Y-%m-%d")
                if foglalas_datum < datetime.now():
                    return "A foglalás dátuma nem lehet múltbeli."
                vegso_datum = foglalas_datum + timedelta(days=napok_szama)
                if self.ellenoriz_foglalasok(szoba, foglalas_datum, vegso_datum):
                    foglalas = Foglalas(szoba, foglalas_datum, napok_szama)
                    self.foglalasok.append(foglalas)
                    return foglalas.foglalas_koltseg()
                else:
                    return "A szoba már foglalt ebben az időpontban."
        return "Nincs ilyen szobaszám a szállodában."

    def foglalas_leadas(self, foglalas):
        if foglalas in self.foglalasok:
            self.foglalasok.remove(foglalas)
            return "Foglalás sikeresen törölve."
        else:
            return "Nincs ilyen foglalás."

    def ellenoriz_foglalasok(self, szoba, foglalas_datum, vegso_datum):
        for foglalas in self.foglalasok:
            if foglalas.szoba == szoba:
                if foglalas_datum < foglalas.vegso_datum and vegso_datum > foglalas.foglalas_datum:
                    return False
        return True


class Foglalas:
    def __init__(self, szoba, foglalas_datum, napok_szama):
        self.szoba = szoba
        self.foglalas_datum = foglalas_datum
        self.vegso_datum = foglalas_datum + timedelta(days=napok_szama)

    def foglalas_koltseg(self):
        return self.szoba.osszkoltseg((self.vegso_datum - self.foglalas_datum).days)


# Szálloda, szobák és foglalások feltöltése
hotel = Szalloda("Luxus Hotel")
hotel.uj_szoba(EgyagyasSzoba("1"))
hotel.uj_szoba(EgyagyasSzoba("2"))
hotel.uj_szoba(KetagyasSzoba("3"))

# Foglalások
hotel.foglalas("1", "2024-04-25", 3)
hotel.foglalas("2", "2024-04-27", 2)
hotel.foglalas("3", "2024-04-29", 4)
hotel.foglalas("1", "2024-05-02", 5)
hotel.foglalas("2", "2024-05-06", 2)


# Felhasználói interfész
def foglalas_felvetel():
    szobaszam = input("Kérem, adja meg a foglalni kívánt szoba számát (1-60:Egyágyas - 61-120:Kétágyas): ")

    # Ellenőrizze, hogy az adott szoba létezik-e és milyen típusú
    szoba = None
    for s in hotel.szobak:
        if s.szobaszam == szobaszam:
            szoba = s
            break

    if szoba is None:
        print("Nincs ilyen szoba.")
        return

    if isinstance(szoba, EgyagyasSzoba):
        print("Az adott szoba Egyágyas.")
    elif isinstance(szoba, KetagyasSzoba):
        print("Az adott szoba Kétágyas.")
    else:
        print("Ismeretlen típusú szoba.")
        return

    while True:
        datum_input = input("Kérem, adja meg a foglalás dátumát (ÉÉÉÉ-HH-NN formátumban): ")
        try:
            datum = datetime.strptime(datum_input, "%Y-%m-%d")
            if datum < datetime.now():  # Ellenőrizzük, hogy a megadott dátum későbbi-e, mint a jelenlegi dátum
                print("A foglalás dátuma nem lehet múltbeli.")
                continue
            break
        except ValueError:
            print("Hibás formátum, kérlek próbáld újra!")

    napok_szama = int(input("Kérem, adja meg a foglalás hosszát napokban: "))

    print(hotel.foglalas(szobaszam, datum.strftime("%Y-%m-%d"), napok_szama))


def foglalas_leadas():
    if not hotel.foglalasok:  # Ha nincs egyetlen foglalás sem
        print("Jelenleg nincsen foglalás!")
        return

    szobaszam = input("Kérem, adja meg a lemondani kívánt foglalás szoba számát: ")
    datum = input("Kérem, adja meg a foglalás dátumát (ÉÉÉÉ-HH-NN formátumban): ")
    for foglalas in hotel.foglalasok:
        if foglalas.szoba.szobaszam == szobaszam and foglalas.foglalas_datum.strftime("%Y-%m-%d") == datum:
            print(hotel.foglalas_leadas(foglalas))
            return
    print("Nincs ilyen foglalás.")


def foglalasok_listazasa():
    print("Foglalások:")
    for i, foglalas in enumerate(hotel.foglalasok, 1):
        print(
            f"{i}. Szoba: {foglalas.szoba.szobaszam}, Dátum: {foglalas.foglalas_datum.strftime('%Y-%m-%d')}, Napok száma: {foglalas.vegso_datum - foglalas.foglalas_datum}")


while True:
    print("\nVálasszon műveletet:")
    print("1. Foglalás felvétele")
    print("2. Foglalás lemondása")
    print("3. Foglalások listázása")
    print("4. Kilépés")

    valasztas = input("Kérem, adja meg a választott művelet sorszámát: ")

    if valasztas == "1":
        foglalas_felvetel()
    elif valasztas == "2":
        foglalas_leadas()
    elif valasztas == "3":
        foglalasok_listazasa()
    elif valasztas == "4":
        print("Kilépés...")
        break
    else:
        print("Nincs ilyen művelet! Kérem, válasszon másik számot.")
