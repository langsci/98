# -*- coding: utf-8 -*-

import re
import pprint

class Entry():
  def __init__(self,a): 
    for l in a:
      l = l.strip()
      if l.endswith('%'):
        l = l[:-1]      
      if 'lsgloss' in l:
        self.gloss = l[9:][:-1]
      elif 'definition' in l:
        self.gloss = l[12:][:-1]     
      if r'\headword' in l:
        try:
          self.vernaculars.append(l)
        except AttributeError:
          self.vernaculars = [l]
        continue            
      if l.strip().startswith(r'\synpos') or l.strip().startswith(r'\pos'):
        try:
          self.poss.append(l)
        except AttributeError:
          self.poss = [l]
          continue
       
d = {}

entries = open('chapters/dictionary.tex').read().decode('utf8').split('%------------------------------')
print len(entries)
for e in entries[1:]:
  #print e
  a = e.split('\n')[1:]
  x = Entry(a)
  pprint.pprint(x.__dict__)
  
  try:
    for g in x.gloss.split(';'): 
      try:
        d[g.strip()].append(x)
      except KeyError:
        d[g.strip()] = [x]
      except AttributeError:     
        s =  u"%% no gloss for %s" % x.vernaculars
        print s.encode('utf8')
  except AttributeError:
    continue

pprint.pprint(d)

for k in sorted(d.keys(),key=lambda s: s.lower()):
  print '%'+30*'-'
  print '\\newentry'
  print u'\\lsgloss{%s}' % k.strip().encode('utf8')
  out = []
  for e in d[k]:
    try:
      out.append(''.join(['~'.join(l)
      for l in zip(e.vernaculars,e.poss)]))      
    except AttributeError:
      print "%%insufficient information for %s".encode('utf8') % k
  print ';\n'.join(out).encode('utf8')      
  