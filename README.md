param\_generator
================

# Example

Prepare your configuration.

```yaml

# Single value
steps: 1000   # 1000
name: sample  # "sample"

# Range
N: 1..3       # 1, 2, 3

# Lispace
L: 10..100/5  # 10.0, 32.5, 55.0, 77.5, 100.0

# List
type:         # "A", "B"
  - A
  - B
region:       # 1, 2, 3, 101, 102, 103
  - 1..3
  - 101..103
```

Confirm your configuration is parsed correctly.

```bash
python main.py --input sample.yml --show

# steps: [1000]
# region: [1, 2, 3, 101, 102, 103]
# type: ['A', 'B']
# L: [10.0, 32.5, 55.0, 77.5, 100.0]
# N: [1, 2, 3]
```

Generate.

```bash
mkdir project
python main.py --input sample.yml --output="project/run{0:04d}/param.yml"
```

You will find many directories under `project`. Each directory contains
`param.yml`.
