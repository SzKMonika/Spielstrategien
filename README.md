# Einführung

Dieses Projekt bietet ein kleines Framework um Spielalgorithmen bei verschiedenen endlichen 2-Personen Spielen mit perfekter Information auszuprobieren.
Eine generelle Vereinbarung ist, dass bei einem ungültigen Zug, der gegen die Regeln verstösst, der andere Spieler gewinnt.
Die aktuell verfügbaren Spiele werden weiter unten kurz beschrieben. Durch das Framework ist es möglich neue ähnliche Spiele relativ einfach hinzuzufügen und in der gleichen Art und Weise spielbar zu machen.

## Wie spielt man?
Das Code wurde in Python geschrieben und kann sowohl in [TigerJython](https://www.tigerjython.ch/) als auch in [Visual Studio Code](https://code.visualstudio.com/) ausgeführt werden. Das Code ist in einem [GitHub Repository](https://github.com/SzKMonika/Spielstrategien) verfügbar und kann auch direkt [als ZIP-Datei heruntergeladen](https://github.com/SzKMonika/Spielstrategien/archive/refs/heads/main.zip) werden.

Für Visual Studio Code gibt es noch einige Voraussetzungen, damit alles gut funktioniert:
* Installiere das [Python Extension for VS Code und auch Python selber](https://code.visualstudio.com/docs/python/python-tutorial#_prerequisites).
* Optional kann man auch noch die GitLens-Erweiterung installieren, ist aber nicht notwendig.
* Zuletzt sollte man in dem Verzeichnis, wohin man dieses Code heruntergeladen hat, folgenden Befehl in einem Terminal ausführen: `pip install -r requirements.txt` (das installiert das benötigte keyboard Package).

Die eigenen Strategien müssen in die Datei `strategy.py` geschrieben werden als Funktionen. Die Funktionen haben immer ein Argument (`game`) und der Name muss abhängig vom Spiel mit *nim_*, *nimMulti_*, *kalaha_*, *vierGewinnt_* oder *mastermind_* anfangen. Nachdem die gewünschten eigenen Strategien erstellt und gespeichert wurden, kann man das Framework mittels `main.py` starten und dort durch entsprechende Eingabe von Zahlen konfigurieren und das ausgewählte Spiel mit den gewählten Strategien laufen lassen.

Die Strategien selber können durch das Argument `game` auf die Properties und evtl. Hilfsmethoden der einzelnen Spiele zugreifen. Weitere Details dazu sind in [strategy.py](docs/strategy.html) und in den einzelnen Modulen unter [games](docs/games.html) beschrieben.

# Spiele
## Nim
Zwei Spieler nehmen abwechselnd eine limitierte Anzahl (z.B. 1, 2 oder 3) von Gegenständen, etwa Streichhölzer, weg. Gewonnen hat beim Standardspiel derjenige, der das letzte Hölzchen nimmt, bei der Misère-Variante verliert dieser.

Die vordefinierten Computer-Strategien sind: `level1`, `level2` und `level3`.

## Nim-Multi
In dieser Variante des Nim-Spiels gibt es mehrere Reihen von Hölzchen, und die zwei Spieler nehmen abwechselnd eins oder mehrere Hölzchen aus einer der Reihen weg. Wie viele sie nehmen, spielt keine Rolle; es dürfen bei einem Zug jedoch nur Hölzchen aus einer einzigen Reihe genommen werden. Gewonnen hat beim Standardspiel derjenige, der das letzte Hölzchen nimmt, bei der Misère-Variante verliert dieser.

Die vordefinierten Computer-Strategien sind: `level1`, `level2` und `level3`.

## Vier gewinnt (Four in a row)
Das Spiel wird auf einem senkrecht stehenden hohlen Spielbrett gespielt, in das die Spieler abwechselnd ihre Spielsteine fallen lassen. Das Spielbrett besteht aus sieben Spalten (senkrecht) und sechs Reihen (waagerecht). Jeder Spieler besitzt 21 gleichfarbige Spielsteine. Wenn ein Spieler einen Spielstein in eine Spalte fallen lässt, besetzt dieser den untersten freien Platz der Spalte. Gewinner ist der Spieler, der es als erster schafft, vier oder mehr seiner Spielsteine waagerecht, senkrecht oder diagonal in eine Linie nebeneinander zu bringen.
*In diesem Spiel ist ein unentschieden möglich, falls das Spielbrett voll wird, bevor jemand gewinnt.*

Die vordefinierten Computer-Strategien sind: `level1`, `level2`, `level3` und `level4`.

## Kalaha
Das Kalaha-Spielbrett besteht aus zwei Muldenreihen mit jeweils sechs Spielmulden plus eine Gewinnmulde jeweils auf der rechten Seite des Spielers. Am Anfang legt man in jede Spielmulde gleich viele, z.B. 4 Steine. Die Spieler bewegen die Steine so, dass aus einer eigenen Spielmulde alle Steine genommen werden, und diese gegen Uhrzeigersinn auf die folgenden Mulden verteilt werden (ausser gegnerische Gewinnmulde). Wenn der letzte Stein in der eigenen Gewinnmulde landet gibt es einen Bonus-Zug, sonst kommt der andere Spieler.
Es gibt noch einen Spezialfall: Wenn der letzte Stein in einer eigenen leeren Spielmulde landet, und direkt gegenüber 1 oder mehr Steine liegen, dann werden alle Steine aus beiden Mulden in die eigene Gewinnmulde verschoben. Das Spiel endet wenn nach einem Zug die Spielmulden auf einer Seite ganz leer werden.
Es gewinnt derjenige Spieler, der mehr Steine auf seiner Seite (inkl. Gewinnmulde) gesammelt hat, bei Gleichstand ist es unentschieden.

Die vordefinierten Computer-Strategien sind: `level1`, `level2a`, `level2b`, `level2c` und `level3`.

## Mastermind
Das ist ein eigenständiges Zweipersonen-Spiel, das jedoch asymmetrisch mit imperferkter Information ist. Wie im echten Mastermind, muss der erste Spieler eine geheime Reihenfolge ausdenken und der zweite Spieler muss diese erraten. Die Reihenfolge besteht in diesem Spiel aus Ziffern (0 bis 9) statt Farben (wie im echten Mastermind).
Nach jedem Tipp gibt der erste Spieler dem zweiten an, wie viele Ziffern richtig sind und an guter Stelle sich befinden, und wie viele an falscher Stelle sind.

Die vordefinierten Computer-Strategien sind: `level2` und `level3`.
