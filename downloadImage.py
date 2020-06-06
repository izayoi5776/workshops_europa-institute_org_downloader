# coding: UTF-8
import urllib.request, urllib.error
from multiprocessing import Pool
import os
import functools
import json
import re
from PIL import Image

# download image parts and merge to a full version
def downloadImg2(base, url, filename, width, height):
  # url = "https://iiif.directories.europa-institute.org/image/294849_0000/full/full/0/native.jpg"
  # target https://iiif.directories.europa-institute.org/image/294849_0000/0,2048,1024,1024/1024,/0/default.jpg
  #                                                                        x y    w    h    w
  url2 = url.replace("full/full/0/native.jpg", "")
  #print("downloadImg2 base=" + base + " url=" + url + " filename=" + filename + " width=" + str(width) + " height=" + str(height))
  
  failmsg = ""

  img = Image.new('RGB', (width, height))
  for x in range(0, width, 1024):
    for y in range(0, height, 1024):
      w = 1024 if x+1024<width else width-x
      h = 1024 if y+1024<height else height-y
      u = url2 + str(x) + "," + str(y) + "," + str(w) + "," + str(h) + "/" + str(w) + ",/0/default.jpg"
      try:
        c = Image.open(urllib.request.urlopen(u))
        print("downloadImg2 " + u + " OK")
        img.paste(c, (x, y))
      except Exception as ex:
        print("downloadImg2 " + u + " FAILED")
        failmsg = " with fails"
  img.save(filename)
  img.close()
  print("downloadImg2 url=" + url + " => " + filename + " MERGED" + failmsg)

# true if file size > 0
def chkImg(fn):
  try:
    if os.path.getsize(fn) > 0:
      return True
  except Exception as ex:
      print(ex)
  return False    

# download
def downloadImg(base, url, width, height):
  # base = 170035
  # url = "https://iiif.directories.europa-institute.org/image/308472_0000/full/full/0/native.jpg"
  path = os.path.join(os.path.abspath(os.path.dirname(__file__)), str(base))
  n = re.search(r'/image/(\d+)_0000/full/full', url).group(1)
  name = os.path.join(path, str(n) + ".jpg")

  os.makedirs(path, exist_ok=True)
  if os.path.exists(name) and chkImg(name):
    print("skip     " + url + " => " + name)
  else:
    try:
      urllib.request.urlretrieve(url, name)
      print("download " + url + " => " + name)
    except Exception:
      print("download " + url + " -- FAILED")

  if not chkImg(name):
    downloadImg2(base, url, name, width, height)


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
          urls.append([j3['resource']['@id'], j3['resource']['width'], j3['resource']['height']])
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
      for [url, width, height] in p.imap(f, urls):
        downloadImg(str(n), str(url), width, height)
