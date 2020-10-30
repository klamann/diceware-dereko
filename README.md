# German Diceware Word List

A decent [Diceware](https://en.wikipedia.org/wiki/Diceware) word list in German, based on [DeReKo](https://www1.ids-mannheim.de/kl/projekte/methoden/derewo.html) data. Contains 6^5 (7776) words, selected from the most frequently used word forms in the German language, filtered for usability in a [passphrase](https://en.wikipedia.org/wiki/Passphrase), e.g. no use of umlauts or very long words.

This list is intended to be an alternative to the popular German word list that can be found on [The Diceware Passphrase Home Page](https://theworld.com/~reinhold/diceware.html), which comes with a few major flaws: many two-letter strings that are no German words, lots of numbers and special characters, misspelled words and highly unusual words and word forms. This word list only consists of actual German words that are in common use and (hopefully) easier to remember. Because [life is too short to remember unnecessarily complex passwords](https://xkcd.com/936/).

## The List

This word list was compiled from the [DeReKo 2014](https://www1.ids-mannheim.de/kl/projekte/methoden/derewo.html) term frequency list which is provided by the [Leibniz-Institut für Deutsche Sprache](https://www1.ids-mannheim.de/) under a Creative Commons License ([CC BY-NC 3.0](https://creativecommons.org/licenses/by-nc/3.0/)). Here is the word list in plain text and json format:

* [`diceware-dereko.txt`](./diceware-dereko.txt) (~110 kb)
* [`diceware-dereko.json`](./diceware-dereko.json) (~170 kb)

*Copyright notice: these documents are derived from work of the Leibniz-Institut für Deutsche Sprache, which was published under [CC BY-NC 3.0](https://creativecommons.org/licenses/by-nc/3.0/). If the compilation of this word list can be seen as fair dealing or fair use in your jurisdiction, then I hereby release it to the public domain. Otherwise the restrictions of the original CC BY-NC 3.0 license apply. In any case, I waive any copyright for my part of the work (see [LICENSE](./LICENSE)).*

## Selection Process

The words in this list were carefully selected from a compilation of the most frequently used word forms in German writing, at least according to the [DeReKo 2014](https://www1.ids-mannheim.de/kl/projekte/methoden/derewo.html) word frequency list. Before the final selection was made, some more filters were applied to this list:

* only include words that match the following [POS tags](https://en.wikipedia.org/wiki/Part-of-speech_tagging): NN, VVFIN, VVINF, ADJD, ADV. These are nouns, adjectives, adverbs and certain verb forms. We exclude named entities and a lot of terms that are important for the language but have no meaning on their own.
* only include words that consist of 3 to 10 characters (less typing, yay).
* avoid characters that are common in German but often not allowed in passwords, like [umlauts](https://en.wikipedia.org/wiki/Umlaut_(linguistics)), [eszett](https://en.wikipedia.org/wiki/%C3%9F) and all kinds of punctuation. Instead of using transliterations to ASCII (e.g. "über" -> "ueber") that might feel non-intuitive for native speakers, these tokens are simply removed.
* filter out certain sensitive terms. Germans don't curse that much in written publications, so there's not much to do here, but obviously we have to deal with Nazis 🙄
* group all tokens by their normalized forms and only include the most frequently used instance of each form. This helps to avoid redundancy and removes less memorable inflexions of many words from the list.
* store all words in lowercase

## Examples

A few random passphrases generated from this word list. Please don't use any of these as your new passphrase ;)

* oldtimer, grill, brach, boot, reflex
* netzwerk, schaller, rechtsweg, ernst, kanonen
* kram, motivieren, speichern, juli, symptome
* einzelfall, locker, ersatzlos, versehen, niedergang
* heilen, grillen, hinauf, reinheit, gesetzlich
* fatal, artillerie, auswertung, gegenwehr, einhaltung
* kragen, lupe, notenbank, port, ausdehnung
* hanseaten, trauben, stadtteil, ackerbau, metall
* korruption, antrieb, judoka, reinigen, gestatten
* stirn, lust, bestechung, naht, notfalls

## License

Developed with ❤ by Sebastian Straub <sstraub [at] posteo.de>

This is free and unencumbered software released into the public domain, see [LICENSE](./LICENSE). The data that the word list was derived from was released by Leibniz-Institut für Deutsche Sprache under [CC BY-NC 3.0](https://creativecommons.org/licenses/by-nc/3.0/)
