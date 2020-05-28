
# find book start point
### Propose
  chk url(https://workshops.europa-institute.org/mirador/n) exists one by one
  
### Usage
  python3 a.py
  
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
with Pool(1) as p:
```

after
```python
with Pool(2) as p:  
```

# download jpg


