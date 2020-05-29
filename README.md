
# find book start point then download images
### Propose
  chk url(https://workshops.europa-institute.org/mirador/n) exists one by one
  
### Usage

```bash
python3 chk.py            # search for book start point, save to good.txt
python3 downloadJson.py   # download json for books in good.txt
python3 downloadImage.py  # download image for books in good.txt
```
  
### Monitoring result
  tail -f good.txt num.txt
  
### Stop
  Ctrl+c to stop any time
  
### Restart
  re-run with num.txt in same directory
  * not very correct when in multi-process mode

### Multi-process
  change line 17, Pool(n) as you need
  
Ex

before
```python
with Pool(10) as p:
```

after
```python
with Pool(20) as p:  
```

