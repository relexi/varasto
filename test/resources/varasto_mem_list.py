# Diese erste Version speichert alle Daten nur in eine Liste im Speicher
# Keine Daten werden permanent auf die Festplatte geschrieben

varasto = []


class Valine:
    """
    Description of Valine

    Attributes:
        paikka (object of class Paikka): location of the valine
        no (string): inventory-number (TREVTAM)
        nimi (string): descriptive name
        luokka (string): subclass of the valine in system

    Args:
        paikka (object of class Paikka):
        no (string):
        nimi (string):
        luokka (string):
    """

    def __init__(self, paikka, no, nimi, luokka):
        self.paikka = paikka
        self.no = no
        self.nimi = nimi
        self.luokka = luokka

    def print_valine(self):
        """
        method that prints the attributes of the object valine

        Args:
            self (undefined):

        """
        print(self.no + " " + self.nimi + " on paikalla " +
              self.paikka.hylly + str(self.paikka.taso) +
              str(self.paikka.vali) + self.paikka.lava)

    def varastoon_valine(self, p):
        """
        method that appends the object to the list of objects
        in the varasto-list

        Args:
            self (undefined):
            p (object of class Paikka): location

        """
        self.paikka = p
        varasto.append(self)


class Paikka:
    def __init__(self, hylly, taso, vali, lava):
        self.hylly = hylly
        self.taso = taso
        self.vali = vali
        self.lava = lava


def varastoi_valine():
    taNo = input("Välineen Numero: ")
    luokkaStr = input("Välineen luokka: ")
    nimiStr = input("Välineen kuvaus: ")
    p = kysyPaikka()
    v = Valine(p, taNo, nimiStr, luokkaStr)
    v.varastoon_valine(p)
    print("varastoitu:")
    v.print_valine()


def naytaValine():
    v = etsiValine()
    v.print_valine()


def kaikkiValineet():
    for v in varasto:
        v.print_valine()


def siirryValine():
    v = etsiValine()
    index = varasto.index(v)
    v.paikka = kysyPaikka()
    varasto[index] = v
    v.print_valine()


def etsiValine():
    taNo = input("Välineen numero: ")
    for v in varasto:
        if v.no == taNo:
            return v


def kysyPaikka():
    paikkaStr = input("Välineen paikka: Hylly,Taso,Väli,Lava: ")
    p = Paikka(paikkaStr[0], paikkaStr[1], paikkaStr[2], paikkaStr[3])
    return p


while True:
    print("-v-arastoi, -n-äytä, -k-aikki, -s-iirry -q-uit")
    kasky = input(">?>  ")
    menu = {
        "v": varastoi_valine,
        "n": naytaValine,
        "k": kaikkiValineet,
        "s": siirryValine,
        "q": quit
    }
    func = menu.get(kasky)
    func()
