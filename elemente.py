#!/usr/bin/env python3
"""
elemente.py - Woerter aus chemischen Elementsymbolen

Zerlegt Woerter vollstaendig in Elementsymbole (z.B. PoSITiVISmUS)
und sucht in einer Wortliste fuer jedes Element ein Beispielwort.

Verwendung:
    python3 elemente.py wort POSITIVISMUS
        -> zerlegt ein einzelnes Wort (falls moeglich)

    python3 elemente.py liste wortliste.txt
        -> findet fuer jedes Element ein Wort aus der Liste
           (Wortliste: eine Datei mit einem Wort pro Zeile,
            z.B. /usr/share/dict/ngerman nach "zypper in words-de")

    python3 elemente.py alle wortliste.txt
        -> gibt ALLE zerlegbaren Woerter der Liste aus

    python3 elemente.py top wortliste.txt [Anzahl]
        -> die Woerter mit den meisten Elementsymbolen (Standard: 25)
"""

import sys
import unicodedata

# Alle 118 Elemente: Symbol -> deutscher Name
ELEMENTE = {
    "H": "Wasserstoff", "He": "Helium", "Li": "Lithium", "Be": "Beryllium",
    "B": "Bor", "C": "Kohlenstoff", "N": "Stickstoff", "O": "Sauerstoff",
    "F": "Fluor", "Ne": "Neon", "Na": "Natrium", "Mg": "Magnesium",
    "Al": "Aluminium", "Si": "Silicium", "P": "Phosphor", "S": "Schwefel",
    "Cl": "Chlor", "Ar": "Argon", "K": "Kalium", "Ca": "Calcium",
    "Sc": "Scandium", "Ti": "Titan", "V": "Vanadium", "Cr": "Chrom",
    "Mn": "Mangan", "Fe": "Eisen", "Co": "Cobalt", "Ni": "Nickel",
    "Cu": "Kupfer", "Zn": "Zink", "Ga": "Gallium", "Ge": "Germanium",
    "As": "Arsen", "Se": "Selen", "Br": "Brom", "Kr": "Krypton",
    "Rb": "Rubidium", "Sr": "Strontium", "Y": "Yttrium", "Zr": "Zirconium",
    "Nb": "Niob", "Mo": "Molybdaen", "Tc": "Technetium", "Ru": "Ruthenium",
    "Rh": "Rhodium", "Pd": "Palladium", "Ag": "Silber", "Cd": "Cadmium",
    "In": "Indium", "Sn": "Zinn", "Sb": "Antimon", "Te": "Tellur",
    "I": "Iod", "Xe": "Xenon", "Cs": "Caesium", "Ba": "Barium",
    "La": "Lanthan", "Ce": "Cer", "Pr": "Praseodym", "Nd": "Neodym",
    "Pm": "Promethium", "Sm": "Samarium", "Eu": "Europium",
    "Gd": "Gadolinium", "Tb": "Terbium", "Dy": "Dysprosium",
    "Ho": "Holmium", "Er": "Erbium", "Tm": "Thulium", "Yb": "Ytterbium",
    "Lu": "Lutetium", "Hf": "Hafnium", "Ta": "Tantal", "W": "Wolfram",
    "Re": "Rhenium", "Os": "Osmium", "Ir": "Iridium", "Pt": "Platin",
    "Au": "Gold", "Hg": "Quecksilber", "Tl": "Thallium", "Pb": "Blei",
    "Bi": "Bismut", "Po": "Polonium", "At": "Astat", "Rn": "Radon",
    "Fr": "Francium", "Ra": "Radium", "Ac": "Actinium", "Th": "Thorium",
    "Pa": "Protactinium", "U": "Uran", "Np": "Neptunium",
    "Pu": "Plutonium", "Am": "Americium", "Cm": "Curium",
    "Bk": "Berkelium", "Cf": "Californium", "Es": "Einsteinium",
    "Fm": "Fermium", "Md": "Mendelevium", "No": "Nobelium",
    "Lr": "Lawrencium", "Rf": "Rutherfordium", "Db": "Dubnium",
    "Sg": "Seaborgium", "Bh": "Bohrium", "Hs": "Hassium",
    "Mt": "Meitnerium", "Ds": "Darmstadtium", "Rg": "Roentgenium",
    "Cn": "Copernicium", "Nh": "Nihonium", "Fl": "Flerovium",
    "Mc": "Moscovium", "Lv": "Livermorium", "Ts": "Tenness",
    "Og": "Oganesson",
}

# Kleingeschriebene Symbole fuer den Vergleich
SYM_LOWER = {s.lower(): s for s in ELEMENTE}


def normalisieren(wort):
    """Umlaute/Akzente aufloesen (ae, oe, ue, ss) und kleinschreiben."""
    w = wort.strip().lower()
    w = (w.replace("\u00e4", "ae").replace("\u00f6", "oe")
          .replace("\u00fc", "ue").replace("\u00df", "ss"))
    # uebrige Akzente (é usw.) entfernen
    w = unicodedata.normalize("NFKD", w)
    w = "".join(c for c in w if c.isascii() and c.isalpha())
    return w


def erreichbarkeit(w):
    """DP: vor[i] = Position i vom Anfang erreichbar,
           nach[i] = vom Punkt i aus ist das Wortende erreichbar."""
    n = len(w)
    vor = [False] * (n + 1)
    vor[0] = True
    for i in range(n):
        if not vor[i]:
            continue
        for L in (1, 2):
            if i + L <= n and w[i:i + L] in SYM_LOWER:
                vor[i + L] = True
    nach = [False] * (n + 1)
    nach[n] = True
    for i in range(n - 1, -1, -1):
        for L in (1, 2):
            if i + L <= n and w[i:i + L] in SYM_LOWER and nach[i + L]:
                nach[i] = True
    return vor, nach


def zerlegbar(w):
    vor, nach = erreichbarkeit(w)
    return vor[len(w)] if w else False


def nutzbare_elemente(w):
    """Alle Symbole, die in IRGENDEINER gueltigen Zerlegung vorkommen."""
    vor, nach = erreichbarkeit(w)
    gefunden = set()
    for i in range(len(w)):
        if not vor[i]:
            continue
        for L in (1, 2):
            if i + L > len(w):
                continue
            teil = w[i:i + L]
            if teil in SYM_LOWER and nach[i + L]:
                gefunden.add(SYM_LOWER[teil])
    return gefunden


def zerlegung(w, muss_enthalten=None):
    """Eine gueltige Zerlegung finden; optional eine, die ein
       bestimmtes Symbol enthaelt. Bevorzugt lange Symbole."""
    vor, nach = erreichbarkeit(w)
    n = len(w)

    def pfad(start, ende):
        """Beliebiger Symbolpfad von start nach ende (greedy, 2 vor 1)."""
        weg, i = [], start
        while i < ende:
            for L in (2, 1):
                teil = w[i:i + L]
                if i + L <= ende and teil in SYM_LOWER:
                    # pruefen, ob von i+L aus 'ende' noch erreichbar ist
                    rest_ok = (i + L == ende) or _erreicht(i + L, ende)
                    if rest_ok:
                        weg.append(SYM_LOWER[teil])
                        i += L
                        break
            else:
                return None
        return weg

    # Hilfstabelle: von Position a nach Position b erreichbar?
    reich = [[False] * (n + 1) for _ in range(n + 1)]
    for a in range(n + 1):
        reich[a][a] = True
        for i in range(a, n):
            if not reich[a][i]:
                continue
            for L in (1, 2):
                if i + L <= n and w[i:i + L] in SYM_LOWER:
                    reich[a][i + L] = True

    def _erreicht(a, b):
        return reich[a][b]

    if not reich[0][n]:
        return None

    if muss_enthalten:
        ziel = muss_enthalten.lower()
        L = len(ziel)
        for i in range(n - L + 1):
            if w[i:i + L] == ziel and reich[0][i] and reich[i + L][n]:
                return pfad(0, i) + [SYM_LOWER[ziel]] + pfad(i + L, n)
        return None
    return pfad(0, n)


def formatieren(symbole):
    return "".join(symbole)


def cmd_wort(wort):
    w = normalisieren(wort)
    z = zerlegung(w)
    if z is None:
        print(f"'{wort}' laesst sich NICHT in Elementsymbole zerlegen.")
        return
    print(f"{wort}  ->  {formatieren(z)}")
    for s in z:
        print(f"  {s:<2}  {ELEMENTE[s]}")


def lade_woerter(pfad):
    woerter = []
    with open(pfad, encoding="utf-8", errors="ignore") as f:
        for zeile in f:
            wort = zeile.split("/")[0].strip()  # hunspell-Flags abschneiden
            if len(wort) >= 2 and wort.isalpha():
                woerter.append(wort)
    return woerter


def cmd_liste(pfad):
    woerter = lade_woerter(pfad)
    # fuer jedes Element das kuerzeste "richtige" Wort sammeln;
    # Abkuerzungen (alles gross, sehr kurz) nur als Notloesung
    beste = {}      # Symbol -> (rang, laenge, originalwort, normiert)
    for wort in woerter:
        w = normalisieren(wort)
        if len(w) < 2:
            continue
        elems = nutzbare_elemente(w)
        if not elems:
            continue
        # Rang 0 = richtiges Wort, Rang 1 = Abkuerzung/Kurzwort
        rang = 0 if (len(w) >= 4 and not wort.isupper()) else 1
        for s in elems:
            alt = beste.get(s)
            if alt is None or (rang, len(w)) < (alt[0], alt[1]):
                beste[s] = (rang, len(w), wort, w)

    gefunden = 0
    for s in sorted(ELEMENTE, key=lambda x: (len(x), x)):
        eintrag = beste.get(s)
        if eintrag is None:
            print(f"{s:<2} ({ELEMENTE[s]:<14}): -- kein Wort gefunden --")
            continue
        gefunden += 1
        _, _, original, w = eintrag
        z = zerlegung(w, muss_enthalten=s)
        print(f"{s:<2} ({ELEMENTE[s]:<14}): {formatieren(z)}   [{original}]")
    print(f"\n{gefunden} von {len(ELEMENTE)} Elementen abgedeckt "
          f"({len(woerter)} Woerter geprueft)")


def cmd_alle(pfad):
    woerter = lade_woerter(pfad)
    n = 0
    for wort in woerter:
        w = normalisieren(wort)
        if len(w) >= 2 and zerlegbar(w):
            z = zerlegung(w)
            print(f"{formatieren(z):<30} [{wort}]")
            n += 1
    print(f"\n{n} zerlegbare Woerter gefunden")


def cmd_top(pfad, anzahl=25):
    """Die Woerter mit den meisten Elementsymbolen finden."""
    woerter = lade_woerter(pfad)
    treffer = []
    gesehen = set()
    for wort in woerter:
        w = normalisieren(wort)
        if len(w) < 2 or w in gesehen or not zerlegbar(w):
            continue
        gesehen.add(w)
        z = zerlegung(w)
        verschieden = len(set(z))
        treffer.append((len(z), verschieden, wort, z))
    treffer.sort(key=lambda t: (-t[0], -t[1], t[2]))
    print(f"{'Symbole':>7}  {'davon versch.':>13}  Wort")
    print("-" * 60)
    for anz, versch, wort, z in treffer[:anzahl]:
        print(f"{anz:>7}  {versch:>13}  {formatieren(z)}   [{wort}]")
    print(f"\n({len(treffer)} zerlegbare Woerter insgesamt)")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    modus, arg = sys.argv[1], sys.argv[2]
    if modus == "wort":
        cmd_wort(arg)
    elif modus == "liste":
        cmd_liste(arg)
    elif modus == "alle":
        cmd_alle(arg)
    elif modus == "top":
        anzahl = int(sys.argv[3]) if len(sys.argv) > 3 else 25
        cmd_top(arg, anzahl)
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
