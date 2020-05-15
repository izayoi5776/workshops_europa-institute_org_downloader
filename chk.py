# coding: UTF-8
import urllib.request, urllib.error

def tryUrl(n):
  ret = True
  #url = "https://workshops.europa-institute.org/mirador/book.cgi?catno=73340"
  #url = "https://workshops.europa-institute.org/mirador/73340"
  url = "https://workshops.europa-institute.org/mirador/" + str(n)
  try:
    urllib.request.urlopen(url)
  except Exception:
    ret = False
  return ret

def doMain(start):
  for n in range(start, 99999):
    if tryUrl(n):
      with open("good.txt", "ab") as fg:
        fg.write((str(n) + "\n").encode())
    with open("num.txt", "wb") as fn:
      fn.write((str(n)).encode())

# ------------------- MAIN -----------------
'''
Propose
  chk url(https://workshops.europa-institute.org/mirador/n) exists one by one
Usage
  python3 a.py
Monitoring result
  tail -f good.txt num.txt
Stop
  Ctrl+c to stop any time
Restart
  re-run with num.txt in same directory
'''

try:
  with open("num.txt", "rb") as fn:
    start = int(fn.read().decode())
except Exception as e:
    start = 0
doMain(start)
