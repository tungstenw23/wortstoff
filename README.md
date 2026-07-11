# Wortstoff

Das Periodensystem-Wortspiel: Bilde deutsche Woerter vollstaendig aus chemischen
Elementsymbolen (wie **GaRaGe** oder **ScHeIBeNWIScHEr**), beantworte Chemie-Quizfragen
nach dem Berliner Rahmenlehrplan und sammle Punkte.

## Spielen

`wortstoff.html` herunterladen und per Doppelklick im Browser oeffnen.
Keine Installation noetig, laeuft komplett offline (Windows, Linux, Mac, Handy).

## Dateien

| Datei | Zweck |
|---|---|
| `wortstoff.html` | Das komplette Spiel (Pflicht) |
| `woerter_runden.txt` | Rundenwoerter zum Erweitern; im Spiel ueber "Eigene Wortliste laden" einlesbar |
| `bilder_laden.html` | Einmal-Werkzeug: laedt Elementfotos von Wikipedia in eine lokale Datei `elementbilder.js` |
| `elemente.py` | Kommandozeilen-Werkzeug: findet zerlegbare Woerter in Wortlisten (`python3 elemente.py top wortliste.txt`) |
| `elementbilder.txt` | Nachschlagewerk: alle 118 Elemente mit Wikipedia-Links |

Die generierte `elementbilder.js` (Elementfotos) gehoert **nicht** ins Repository -
jeder erzeugt sie sich selbst mit `bilder_laden.html` (Lizenzgruende, Dateigroesse).

## Spielmodi

- **Rundenwoerter:** Das Spiel versteckt ein geheimes Wort vollstaendig in deinen
  Kaertchen - erst 3 Symbole, pro Runde eines mehr bis 8. Finde es! Hinweise kosten
  steigend Punkte, Nebenfunde aus der Wortliste zaehlen ebenfalls.
- **Freies Spiel:** Eigene Woerter aus der Hand legen, Mitspieler entscheiden ueber
  die Gueltigkeit.

Jeder Zug beginnt mit einer Startfrage (Reaktionswissen, gestaffelt nach
Jahrgangsstufen 7/8, 9, Oberstufe) - richtig beantwortet zaehlen die Wortpunkte doppelt.
Zu jedem Element im gelegten Wort folgt eine Zusatzfrage mit Steckbrief
(Atommodell bzw. Teilchenbeschleuniger-Grafik, Entdeckung, Verwendung, Foto).

## Eigene Inhalte

- **Woerter:** eine Textdatei mit einem Wort pro Zeile im Startbildschirm laden -
  das Spiel prueft die Zerlegbarkeit und sortiert die Stufe (3-8 Symbole) selbst ein.
- **Quizfragen:** im Code unter `REAKTIONSFRAGEN` (nach Jahrgangsstufen) ergaenzen.
- **Avatare:** im Code unter `CHEMIKER` ergaenzen.

## Versionierung

Die aktuelle Versionsnummer steht auf dem Startbildschirm des Spiels und sollte
bei jeder Aenderung erhoeht werden (Suche im Code nach "Version").
