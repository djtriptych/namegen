#!/usr/bin/env python

import logging
import random
import re
import sys

def load_grammar(path):

  """ Given a path to a grammar, parse the grammar, and generate a dict where
  heads are keys and valid productions are values represented as sets of
  strings. """

  def stripped (lines):

    """ Trim whitespace from input lines. """

    for line in lines:
      yield line.strip()

  def block_split (lines, p, yield_empty=False):

    """ Yield blocks based on lines matching a predicate. """

    block = []
    for line in lines:
      if p(line):
        if len(block):
          yield block
          block = []
        else:
          if yield_empty:
            yield block
            block = []
      else:
        block += [line]
    else:
      if len(block):
        yield block

  def productions (blocks):

    """ Convert blocks of lines to (head, tail) pairs representing a prodution.
    The head is the non-terminal and the tail is a list of possible productions.
    """

    for block in blocks:
      yield (block[0], block[1:])

  def uncommented (lines):

    """ Strip comments from input. """

    for line in lines:
      if not line.startswith('#'):
        yield line

  def lines (path):

    """ Given a path, generate lines in that file. """

    with open(path) as f:
      for line in f:
        yield line

  lines = uncommented(stripped(lines(path)))
  blocks = block_split(lines, p=lambda line: not line)

  return dict(productions(blocks))

def gen_name(grammar):

   def tokenize(sentence):
     """ Tokenize the grammar rules. """
     # Break on strings of whitespace
     tokens = re.split('\s+', sentence)
     return tokens

   def convert_token(token):

      def is_string(token):
         return token.startswith('"')

      def is_set_name(token):
         return token in grammar

      def unquote(token):
         return token[1:-1]

      def capitalize(phrase):
         for word in phrase.split():
            yield word[0].upper() + word[1:]

      def random_choice(set):
         return random.choice(set)

      if is_set_name(token):
         return ' '.join(list(capitalize(random_choice(grammar[token]))))

      return token

   # Pick a sentence at random, and generate a name.
   sentence = random.choice(grammar['sentences'])

   # TODO: Recursively expand tokens until there are no non-terminals in the list.
   name = ' '.join(convert_token(t) for t in tokenize(sentence))

   logging.info('%s => %s' % (sentence, name))
   return name

if __name__ == '__main__':

  grammar_path = sys.argv[1]
  grammar = load_grammar(grammar_path)

  # Generate some initial values for rap names based on user's name.
  if grammar_path == 'rapname.grammar':
    name = sys.argv[2]
    grammar.update({
      'initial': [name[0]],
      'initialletters': [''.join(c.upper()+'.' for c in name)],
      'name': [name],
    })

  for i in range(10):
    print gen_name(grammar)
