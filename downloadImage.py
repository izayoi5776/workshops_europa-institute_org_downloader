# coding: UTF-8
import urllib.request, urllib.error
from multiprocessing import Pool
import os
import functools
import json
import re

# download
def downloadImg(base, url):
  # base = 170035
  # url = "https://iiif.directories.europa-institute.org/image/308472_0000/full/full/0/native.jpg"
  path = os.path.join(os.path.abspath(os.path.dirname(__file__)), str(base))
  n = re.search(r'/image/(\d+)_0000/full/full', url).group(1)
  name = os.path.join(path, str(n) + ".jpg")

  os.makedirs(path, exist_ok=True)
  if os.path.exists(name):
    print("skip     " + url + " => " + name)
  else:
    try:
      urllib.request.urlretrieve(url, name)
      print("download " + url + " => " + name)
    except Exception:
      print("download " + url + " -- FAILED")


# any good idea?
def f(n):
  return n;

# parse json to img urls
def readJson(base):
  urls = []
  try:
    with open(os.path.join(str(base), str(base)+".json"), "rb") as f:
      jsn = json.load(f)

    for j1 in jsn['sequences']:
      for j2 in j1['canvases']:
        for j3 in j2['images']:
          urls.append(j3['resource']['@id'])
  except Exception as ex:
    print(ex)
  return urls

# main
if __name__ == '__main__':
  # read num for good
  try:
    with open("good.txt", "rb") as fn:
      good = fn.read().decode().split("\n")
  except Exception as ex:
    print(ex)

  # controler
  for n in good:
    urls = readJson(n)
    with Pool(10) as p:
      for url in p.imap(f, urls):
        downloadImg(str(n), str(url))
