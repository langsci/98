 find . -name '*.bib' | xargs grep -h title| grep -o "= *{.*"| sed s/^\.\.// |egrep -o "\{[A-Z][^\} ]+\}"|sort -u 
