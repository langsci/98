import re

class Entry():
  def __init__(self,a):
    for l in a:
      l = l.strip()
      if l.endswith('%'):
        l = l[:-1]   
      if r'\glosses' in l:
        self.gloss = l[9:-1]     
      if r'\citationform' in l:
        try:
          self.vernaculars.append(l)
        except AttributeError:
          self.vernaculars = [l]
        continue            
      if l.strip().startswith(r'\pos'):
        try:
          self.poss.append(l)
        except AttributeError:
          self.poss = [l]
          continue
       
d = {}

entries = open('chapters/dictionary.tex').read().split('%------------------------------') 
for e in entries[1:]:
  #print e
  a = e.split('\n')[1:]
  x = Entry(a)
  try:
    for g in x.gloss.split(';'): 
      try:
        d[g.strip()].append(x)
      except KeyError:
        d[g.strip()] = [x]
      except AttributeError:     
        s =  "%% no gloss for %s" % x.vernaculars
        print(s)
  except AttributeError:
    continue
      
for k in sorted(d.keys(),key=lambda s: s.strip().lower()):
  print('%'+30*'-')
  print('\\newentry')
  print('\\lsgloss{%s}' % k.strip())
  out = []
  for e in d[k]:
    try:
      out.append(''.join(['~'.join(l)
      for l in zip(e.vernaculars,e.poss)]))      
    except AttributeError:
      print("%%insufficient information for %s" % k)
  print(';\n'.join(out))
  