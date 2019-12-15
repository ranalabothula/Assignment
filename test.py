import re

txt = "o CSSJavaScriptHTML"

x = re.split('o\s',txt)

for y in x:
    print(y.strip())

#print(x) ('?:\d.|o\s'), txt