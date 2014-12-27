param\_generator
================

1. Prepare your configuration.
```yaml
n:
  t: int
  v: 1..10      # 1, ..., 10
k:
  t: float
  v: 0..1/10    # 0.0, 0.1, ..., 1.0
```
2. Execute command.
```bash
python main.py --input sample.yml --output="project/run{0:04d}/param.yml"
```
3. You will find parameter files in the directories.
```yaml
# run0000/param.yml
n: 1
k: 0.0
```
```
project0/
| run0000/
| | param.yml
| run0001/
| run0002/
| run0003/
| run0004/
| run0005/
| run0006/
| run0007/
| run0008/
| run0009/
```
