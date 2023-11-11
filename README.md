# audio-research-stuff
Personal research and experimentation with audio

This repo is in disarray! The experiments don't have required dependencies documented.

## Installing

Create virtual environment
```shell
python3.11 -m venv venv
```

Activate virtual environment
```shell
# On Windows
venv\Scripts\activate.bat
# On *nix
. venv/bin/activate
```

Upgrade PIP
```shell
python -m pip install -U pip
```

Install dependencies
```shell
python -m pip install -U -r requirements.txt
```

Create IPython kernel
```shell
python -m ipykernel install --user --name="audio-research-stuff"
```
