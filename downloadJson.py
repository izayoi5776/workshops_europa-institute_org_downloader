# coding: UTF-8
import urllib.request, urllib.error
from multiprocessing import Pool
import os
import functools

def downloadJson(n):
  url = "https://workshops.europa-institute.org/mirador/" + str(n)
  path = os.path.join(os.path.abspath(os.path.dirname(__file__)), str(n))
  name = os.path.join(path, str(n) + ".json")

  os.makedirs(path, exist_ok=True)
  if os.path.exists(name):
    print("skip     " + url + " => " + name)
  else:
    try:
      urllib.request.urlretrieve(url, name)
      print("download " + url + " => " + name)
    except Exception:
      print("download " + url + " -- FAILED")


'''
download json
'''
if __name__ == '__main__':
  try:
    with open("good.txt", "rb") as fn:
      good = fn.read().decode().split("\n")
  except Exception as ex:
    print(ex)

  with Pool(10) as p:
    for n in p.imap(downloadJson, good):
      pass
