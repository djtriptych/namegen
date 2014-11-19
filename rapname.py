#!/usr/bin/env python

"""
Picked this because I'm generally interested in these half-editorial
half-programming living-document content space.

Here, a programmer is assisting an editor in creating a grammar which, given
some input (a user's name) will generate some new string.

It's pretty typical of code I write - lots of dumb data and simple functions,
and hopefully very few tricky parts, which I take care to explain well.

I find it a very beautiful piece of code. It solves an interesting problem AND
there are lots of obvious and interesting ways to amend it for other uses.

Here's what it does. 

Given a user's name, generate a rap name. 

It works by creating a full rap name grammar to rap names, which is augmented
acoording to the users input. 


TODO:
  + Encapsulate rap-name specific stuff.
  + Add celeb name stuff.
  + Specify SETS as a single string which is parsed.
  + Include top-level productions ("sentences") as
  - Differntiate token type (literal / terminal / non-terminal) in grammar
  	syntax.
"""

import logging
import random
import re 
import sys

def load_grammar(path):
  """ Given a path to a grammar, generate a dict where heads are
  keys and valid productions are tails - sets of strings """

  def stripped (lines):
    for line in lines:
    	yield line.strip()

  def block_split (lines, p, yield_empty=False):
    """ Yield blocks based on lines matching a predicate """
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
    for block in blocks:
    	yield (block[0], block[1:])

  def uncommented (lines) :
    for line in lines:
      if not line.startswith('#'):
      	yield line

  def lines (path):
    """ Given a path, gen lines in that file. """
    with open(path) as f:
      for line in f:
      	yield line

  lines = uncommented(stripped(lines(path)))
  blocks = block_split(lines, p=lambda line: not line)
  grammar = dict(productions(blocks))

  return grammar

def gen_name(grammar):

   def tokenize(sentence):
      # Break on strings of whitespace
      tokens = re.split('\s+', sentence)
      return tokens

   def convert_token(token):  
      # Helper functions
      def is_string(token):
         return token.startswith('"')
      def unquote(token):
         return token[1:-1]
      def is_set_name(token):
         return token in grammar
      def get_set(token):
         return grammar[token]
      def capitalize(phrase):  
         for word in phrase.split():
            yield word[0].upper() + word[1:]
      def random_choice(set):
         return random.choice(set)

      if is_string(token):
         return unquote(token)
      if is_set_name(token):
         return ' '.join(list(capitalize(random_choice(get_set(token)))))
      return token

   # Sets that depend on the user's name
   # We amend our grammar by adding terminals that are generated based on the
   # input.
   #
   # In the case of rap names.

   # Pick a sentence at random, and generate a rap name.
   sentence = random.choice(grammar['sentences'])

   # Recursively do this until there are no non-terminals in the list.
   name = ' '.join(convert_token(t) for t in tokenize(sentence))

   logging.info('%s => %s' % (sentence, name))
   return name 
   

if __name__ == '__main__':

  grammar = load_grammar('rapname.grammar')

  name = sys.argv[2]
  grammar_path = sys.argv[1]

  grammar.update({
    'initial': [name[0]],
    'initialletters': [''.join(c.upper()+'.' for c in name)],
    'name': [name],
  })

  for i in range(10):
    print gen_name(grammar)
