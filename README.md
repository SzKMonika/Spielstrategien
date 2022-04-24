# Einführung

Dieses Projekt bietet ein Framework um Spielalgorithmen bei verschiedenen endlichen 2-Personen Spielen mit perfekter Information auszuprobieren.
Eine generelle Vereinbarung ist, dass bei einem ungültigen Zug, der gegen die Regeln verstösst, der andere Spieler gewinnt.
Aktuell werden nachfolgende Spiele unterstützt.

## Wie spielt man?
Die eigene Strategien müssen in die Datei `strategy.py` geschrieben werden als Methoden. Die Methoden haben immer ein Argument (game) und der Name muss abhängig vom Spiel mit *nim_*, *nimMulti_*, *kalaha_*, *vierGewinnt_* oder *mastermind_* anfangen. Nachdem die gewünschten eigenen Strategien erstellt und gespeichert wurden, kann man das Framework mittels `main.py` starten und dort durch entsprechende Eingabe von Zahlen konfigurieren und das ausgewählte Spiel mit den gewählten Strategien laufen lassen.

# Spiele
## Nim
Zwei Spieler nehmen abwechselnd eine limitierte Anzahl (z.B. 1, 2 oder 3) von Gegenständen, etwa Streichhölzer, weg. Gewonnen hat beim Standardspiel derjenige, der das letzte Hölzchen nimmt, bei der Misère-Variante verliert dieser.

### Nim - Strategien
* `level1`: Man nimmt immer eine Zufallszahl zwischen 1 und max (3) an Streichhölzer weg, aber höchstens so viele die noch verfügbar sind.
* `level2`: Die Dumme Strategie kann so erweitert werden, dass wenn es möglich ist genau 0 (Standard) bzw. 1 (Misère) oder um max+1 (4) mehr Streichhölzer stehen zu lassen, dann wird so gezogen.
* `level3`: Man nimmt immer so viele Streichhölzer, dass nachher eine Mehrfache von max+1 (4) plus 0 (Standard) bzw. 1 (Misère) bleiben, oder wenn das nicht geht, dann wird 1 weggenommen.

## Nim-Multi
In dieser Variante des Nim-Spiels gibt es mehrere Reihen von Hölzchen, und die zwei Spieler nehmen abwechselnd eins oder mehrere Hölzchen aus einer der Reihen weg. Wie viele sie nehmen, spielt keine Rolle; es dürfen bei einem Zug jedoch nur Hölzchen aus einer einzigen Reihe genommen werden. Gewonnen hat beim Standardspiel derjenige, der das letzte Hölzchen nimmt, bei der Misère-Variante verliert dieser.

### Nim-Multi - Strategien
* `level1`: Man nimmt immer von einer zufälligen Reihe eine zufällige Anzahl an Streichhölzer weg.
* `level2`: Aus der Reihe mit den meisten Streichhölzer wird immer so gezogen, dass im Anschluss möglichst mind. 1 und gerade (Standard) bzw. ungerade (Misère) Anzahl an Einser-Reihen und 0 oder mind. 2 Reihen mit mehr als 1 Hölzchen stehen bleiben. Wenn die Stellung nicht erreicht werden kann, dann werden in dieser Reihe 2 Hölzchen stehen gelassen.
* `level3`: Man nimmt Streichhölzer so weg, dass nachher eine *Verluststellung* für den Gegner hinterlassen wird. Eine *Verluststellung* erkennt man so, dass die bitweise exklusiv-ODER-Summe der Anzahl Streichhölzer in den einzelnen Reihen 0 ist. Diese Strategie gilt bei der Standard-Variante bis zum Schluss. Bei der Misère-Variante gilt es am Anfang bis zum Zug wo es genau eine Reihe mit mehr als einem Hölzchen gibt. Bei diesem Zug muss man einfach entweder alle oder alle bis auf ein Hölzchen wegnehmen, so dass dem Gegner eine ungerade Anzahl von Einser-Reihen übergeben wird.

## Vier gewinnt (Four in a row)
Das Spiel wird auf einem senkrecht stehenden hohlen Spielbrett gespielt, in das die Spieler abwechselnd ihre Spielsteine fallen lassen. Das Spielbrett besteht aus sieben Spalten (senkrecht) und sechs Reihen (waagerecht). Jeder Spieler besitzt 21 gleichfarbige Spielsteine. Wenn ein Spieler einen Spielstein in eine Spalte fallen lässt, besetzt dieser den untersten freien Platz der Spalte. Gewinner ist der Spieler, der es als erster schafft, vier oder mehr seiner Spielsteine waagerecht, senkrecht oder diagonal in eine Linie nebeneinander zu bringen.
*In diesem Spiel ist ein unentschieden möglich, falls das Spielbrett voll wird, bevor jemand gewinnt.*

### Vier gewinnt - Strategien
* `level1`: Der Spielstein wird in eine zufällige Spalte gelegt.
* `level2`: Alle 7 mögliche Züge werden angeschaut, und wenn man bei einem gewinnen würde, dann wird diese Spalte gewählt. Wenn es keine Gewinner-Spalte gibt, aber man in einer (nicht gewählten) Spalte verlieren würde wenn der Gegner nachher die wählt, dann wird diese Spalte gewählt und blockiert. Ansonsten wird zufällig gewählt.
* `level3`: Ähnlich wie `level2`, aber vor dem letzten zufälliger Wahl wird eher bzw. stattdessen die mittlere Spalte gewählt falls die noch nicht voll ist.
* `level4`: Ähnlich wie `level2`, aber statt dem letzten zufälligen Wahl wird für jede mögliche wählbare Stelle ein Wert kalkuliert, der die Anzahl möglicher 4-er Linien durch diese Stelle angibt, und gewählt wird die Stelle mit dem höchsten Wert. Zudem wird geschaut ob der andere Spieler gewinnen würde, wenn er nachher auch diese Spalte wählt, und falls ja, dann wird die Stelle mit dem zweitgrössten Wert gewählt.

## Kalaha
Das Kalaha-Spielbrett besteht aus zwei Muldenreihen mit jeweils sechs Spielmulden plus eine Gewinnmulde jeweils auf der rechten Seite des Spielers. Am Anfang legt man in jede Spielmulde gleich viele, z.B. 4 Steine. Die Spieler bewegen die Steine so, dass aus einer eigenen Spielmulde alle Steine genommen werden, und diese gegen Uhrzeigersinn auf die folgenden Mulden verteilt werden (ausser gegnerische Gewinnmulde). Wenn der letzte Stein in der eigenen Gewinnmulde landet gibt es einen Bonus-Zug, sonst kommt der andere Spieler.
Es gibt noch einen Spezialfall: Wenn der letzte Stein in einer eigenen leeren Spielmulde landet, und direkt gegenüber 1 oder mehr Steine liegen, dann werden alle Steine aus beiden Mulden in die eigene Gewinnmulde verschoben. Das Spiel endet wenn nach einem Zug die Spielmulden auf einer Seite ganz leer werden.
Es gewinnt derjenige Spieler, der mehr Steine auf seiner Seite (inkl. Gewinnmulde) gesammelt hat, bei Gleichstand ist es unentschieden.

### Kalaha - Strategien
* `level1`: Die Steine aus einer zufällig gewählten Mulde werden weggenommen.
* `level2`: Zuerst schauen wir, ob es einen Zug gibt, der den letzten Stein gerade in den Kalah bringt. Dann schauen wir ob wir mit einem Zug gegnerische Steine erbeuten können. Sonst schauen wir ob auf der anderen Seite leere Mulden gibt und versuchen auf unserer Seite die Mulde mit den meisten Steinen dadurch zu schützen, dass wir unsere Steine von dieser wegbringen. Zuletzt, wenn kein Regel davor gegriffen hat, suchen wir den Zug, der die wenigsten Steine auf die andere Seite bringt.
* `level3`: Ähnlich, wie `level2`, aber im Falle von leerem Mulden auf der anderen Seite prüft die Strategie zusätzlich, ob es nicht möglich ist, in die Mulde ein eigenes Stein zu "legen".

## Mastermind
Das ist ein eigenständiges Zweipersonen-Spiel, das jedoch asymmetrisch mit imperferkter Information ist. Wie im echten Mastermind, muss der erste Spieler eine geheime Reihenfolge ausdenken und der zweite Spieler muss diese erraten. Die Reihenfolge besteht in diesem Spiel aus Ziffern (0 bis 9) statt Farben (wie im echten Mastermind).
Nach jedem Tipp gibt der erste Spieler dem zweiten an, wie viele Ziffern richtig sind und an guter Stelle sich befinden, und wie viele an falscher Stelle sind.

### Mastermind - Strategien
* `level2`: Für jede Stelle wird festgehalten welche Ziffer an der Stelle noch vorkommen können, und darauf basierend wird Ziffer für Ziffer ein zufälliger Tipp generiert. Nach jedem Tipp, in dem keine richtige Ziffer bzw. keine an gute Stelle ist, werden die entsprechenden Ziffer von allen Stellen bzw. von der jeweilige Stelle als mögliche Lösung entfernt, und somit werden die möglichen Ziffer immer weniger. 
* `level3`: Eine relativ gute brute-force Strategie, die eine Liste über die möglichen Geheimzahl-Kandidaten führt, die noch in Frage kommen können. Nach jedem Zug wird für jeden Geheimzahl-Kandidat geprüft, ob diese Zahl verglichen mit dem aktuellen Tipp das gleiche Resultat gibt, und wenn nicht, dann wird diese Zahl aus der Liste entfernt. Nach etwa 5-7 Zügen bleiben dann nur noch sehr wenige oder nur einen möglichen Kandidat übrig.