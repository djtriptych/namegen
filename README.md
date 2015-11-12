Generate funny names.

This is a tiny language for generating funny names.  It was grown from the live 90's rap name project here:
http://hypngcs.appspot.com/rapname

Once you define a language using a very simple format, the program will generate
random sentences in that language. With small modifications, it's possible

I'm interested in this writer/hacker content space.  I'm curious about new kinds
of documents that incorporate the work of both. See also the Questlove Celebrity
Stories here: 
http://hypngcs.appspot.com/questo.

** Understanding .grammar files **

.grammar files are simple ways to build up sentences in your language.
Nerds: this is a lot like a simplified BNF-style grammar if that helps you
along.
  

```
```


**TODO**:
  - [ ] Differentiate token type (literal / terminal / non-terminal) in grammar
    syntax.
  - [ ] Add argument to specify number of names to generate.

  - [x] Encapsulate rap-name specific stuff.
  - [x] Add celeb name stuff.
  - [x] Specify SETS as a single string which is parsed.
  - [x] Include top-level productions ("sentences") as
  - [x] Clean up whitespace.
"""

