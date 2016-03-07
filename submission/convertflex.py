import xml2dic
import sys
import xml.etree.ElementTree as ElementTree

oldtag = ''
oldattr = {}
def process(e, level=0):
    global oldtag, oldattr
    s = ''
    tag = e.tag.strip()	
    if tag in(('Str','AStr')): 
	for child in e:
	    process(child,level=level+1)
	return
    try:	
	text = e.text.strip()
    except AttributeError:
	text = "" 
    attr = e.attrib 
    if tag == 'Run':
	try:
	  out = "\\%s{%s}"% (attr['namedStyle'].replace('-','').replace(' ',''),text)
	except KeyError:
	  out = u'%s\\%s{%s}'%(level*' ',oldtag.replace('_',''),text) 
	  oldtag = tag
	  oldattr = attr
	print out.encode('utf8') 
    else: 
	if oldtag!='Run':
	    out = u'%s\\%s%s{}'%(level*' ',oldtag.replace('_',''),''.join(["[%s]"%oldattr[k] for k in oldattr if k not in (("ws","number"))]))
	    print out.encode('utf8')
	oldtag = tag
	oldattr = attr
	
    for child in e:
	process(child,level=level+1)
	
fn = sys.argv[1]

tree = ElementTree.parse(fn)
root = tree.getroot()
xmldict = xml2dic.XmlDictConfig(root)

for e in root:
    print "%"+30*'='
    process(e)
