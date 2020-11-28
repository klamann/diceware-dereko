# German Diceware Word List

A decent [Diceware](https://en.wikipedia.org/wiki/Diceware) word list in German, based on [DeReKo](https://www1.ids-mannheim.de/kl/projekte/methoden/derewo.html) data. Contains 6^5 (7776) words, selected from the most frequently used word forms in the German language, filtered for usability in a [passphrase](https://en.wikipedia.org/wiki/Passphrase), e.g. no use of umlauts or very long words.

This list is intended to be an alternative to the popular German word list that can be found on [The Diceware Passphrase Home Page](https://theworld.com/~reinhold/diceware.html), which comes with a few major flaws: many two-letter strings that are no German words, lots of numbers and special characters, misspelled words and highly unusual words and word forms. This word list only consists of actual German words that are in common use and (hopefully) easier to remember. Because [life is too short to remember unnecessarily complex passwords](https://xkcd.com/936/).

## The List

This word list was compiled from the [DeReKo 2014](https://www1.ids-mannheim.de/kl/projekte/methoden/derewo.html) term frequency list which is provided by the [Leibniz-Institut für Deutsche Sprache](https://www1.ids-mannheim.de/) under a Creative Commons License ([CC BY-NC 3.0](https://creativecommons.org/licenses/by-nc/3.0/)). Here is the word list in plain text and json format:

* [`diceware-dereko.txt`](https://raw.githubusercontent.com/klamann/diceware-dereko/master/diceware-dereko.txt) (~110 kb)
* [`diceware-dereko.json`](https://raw.githubusercontent.com/klamann/diceware-dereko/master/diceware-dereko.json) (~170 kb)

*Copyright notice: these documents are derived from work of the Leibniz-Institut für Deutsche Sprache, which was published under [CC BY-NC 3.0](https://creativecommons.org/licenses/by-nc/3.0/). If the compilation of this word list can be seen as fair dealing or fair use in your jurisdiction, then I hereby release it to the public domain. Otherwise the restrictions of the original CC BY-NC 3.0 license apply. In any case, I waive any copyright for my part of the work (see [LICENSE](./LICENSE)).*

### Alternative Versions

The main list contains words with up to 10 characters. As an alternative, another list with words that are up to 8 characters long is provided. This should help to generate shorter passphrases without reducing the lower bound for the entropy of each passphrase, which would be more user friendly, but the list may contain a few terms that are a bit more unusual.

You may find the list in the [alternatives folder](./alternatives). The same licensing conditions apply.

## Selection Process

The words in this list were carefully selected from a compilation of the most frequently used word forms in German writing, at least according to the [DeReKo 2014](https://www1.ids-mannheim.de/kl/projekte/methoden/derewo.html) word frequency list. Before the final selection was made, some more filters were applied to this list:

* only include words that match the following [POS tags](https://en.wikipedia.org/wiki/Part-of-speech_tagging): NN, VVFIN, VVINF, ADJD, ADV, VMFIN, VVIMP. These are nouns, adjectives, adverbs and certain verb forms. We exclude named entities, numbers and some other stuff.
* only include words that consist of 3 to 10 characters (there is [another list](./alternatives) with only 3 to 8 characters).
* avoid characters that are common in German but often not allowed in passwords, like [umlauts](https://en.wikipedia.org/wiki/Umlaut_(linguistics)), [eszett](https://en.wikipedia.org/wiki/%C3%9F) and all kinds of punctuation. Instead of using transliterations to ASCII (e.g. "über" -> "ueber") that might feel non-intuitive for native speakers, these tokens are simply removed.
* filter out certain sensitive terms. Germans don't curse that much in written publications, so there's not much to do here, but obviously we have to deal with Nazis 🙄
* group all tokens by their normalized forms and only include the most frequently used instance of each form. This helps to avoid redundancy and removes less memorable inflexions of many words from the list.
* store all words in lowercase

There is also an option to generate a wordlist for 6 dice (instead of 5) with a total of 46656 tokens which deviates from this process. Because this list contains way more redundant and unusual terms, it is not provided in this repo and it is not recommended to use it to create passphrases, but the code to compile the list is there.

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
