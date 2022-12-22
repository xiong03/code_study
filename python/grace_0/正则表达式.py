# coding:utf-8

import re

pattern = r"\B(?=(?:\d{3})+(?!\d))"
repl = ','
text = '1234567890'
m = re.sub(pattern , repl, text)
print(m)