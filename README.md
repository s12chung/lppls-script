# lppls-script

Simple wrapper around https://github.com/Boulder-Investment-Technologies/lppls to easily get the output.


## Local Development and Run

### Setup

```bash
python3 -m venv .
source ./bin/activate
pip install pipx setuptools
```

### Before Development

```bash
source ./bin/activate
```

### Local Install

```bash
pipx install --force .
```

### Local Run

```bash
# this API key only works for BTC/USD
TWELVE_API_KEY=demo lppls-script "BTC/USD"
```