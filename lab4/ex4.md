# Syntactic and dependency parsing in translations

Syntactic and dependency parsing are two basic tools used by many applications that deal with natural language. A prime example are any translation tools as these would require both of these parsing methods for an improved accuracy.


## Syntactic parser

Syntactic parsing is needed in order to understand the overall structure of a sentence. Breaking down sentences in grammatical components helps with properly reordering words to fit the target language rules leading to a more coherent translation. A prime example would be translating sentences from languages that commonly use adjective-noun constructions to languages that use noun-adjective order.

## Dependency parsing
Dependency parsing helps breaking down ambiguity, as it clarifies the relationships between words. This can be especially useful when translating from languages where the position of the words might be less important, where word cases might be more relevant for establishing grammatical roles.

## Conclusion 
In practice, many translation apps can use both of these tools, such as in rule based systems, whereas neural machine translation system could rely on implicitly learning word relations from large amount of data alone. However, hybrid systems that also use parsing to some extent can often achieve better results

