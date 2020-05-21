# coding: UTF-8
import urllib.request, urllib.error
from multiprocessing import Pool
import os
import functools

def downloadOne(url, path, name, quiet=False):
  '''
  ## download url save as path/name
  - download if not exists \n
  - create folder path if not exists \n
  '''
  ret = True
  os.makedirs(path, exist_ok=True)
  if os.path.exists(name) and not quiet:
    print("skip     " + url + " => " + name)
  else:
    try:
      urllib.request.urlretrieve(url, name)
      if not quiet:
        print("download " + url + " => " + name)
    except Exception:
      ret = False
      if not quiet:
        print("download " + url + " -- FAILED")

  return ret

def downloadImg(base, n):
  '''
  - download n-th jpg if needed \n
  '''
  ret = True
  #url = "https://iiif.directories.europa-institute.org/image/20749_0000/full/full/0/native.jpg"
  imgurl = "https://iiif.directories.europa-institute.org/image/" + str(n) + "_0000/full/full/0/native.jpg"
  #jsonurl = "https://workshops.europa-institute.org/mirador/20747"
  jsonurl = "https://workshops.europa-institute.org/mirador/" + str(base)

  path = os.path.join(os.path.abspath(os.path.dirname(__file__)), str(base))
  imgname = os.path.join(path, str(n) + ".jpg")
  jsonname = os.path.join(path, str(base) + ".json")

  ret = downloadOne(jsonurl, path, jsonname, quiet=True) and downloadOne(imgurl, path, imgname)
  return ret

def download(fm, to):
  fun = functools.partial(downloadImg, fm)
  with Pool(10) as p:
    for n in p.imap(fun, range(fm, to)):
      pass



if __name__ == '__main__':
  try:
    with open("good.txt", "rb") as fn:
      start = fn.read().decode().split("\n")
  except Exception as ex:
    print(ex)

  for i in range(0, len(start)-2):
    try:
      fm = int(start[int(i)])
      to = int(start[int(i)+1])
      print("i=" + str(i) + " from=" + str(fm) + " to=" + str(to))
      download(fm, to)
    except Exception as ex:
      print(ex)

