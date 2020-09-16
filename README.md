<p display="flex">
  <img src="media/logo.png" >
</p>
# pyclone

An RClone wrapper for python that comes bundled with rclone 1.53.1. No need to have rclone installed.

## Installation

Run the following to install:

```python
pip install pyclone
```


and thats it.

## Usage

pyclone is a wrapper or rclone, so you can use the same commands you regularly use in rclone

```bash
pyclone config
```

Or if you want to import pyclone into your project, there are a few functions available.

```python
import pyclone

# Create
pyclone.create('drive', 'drive_name', 'user', 'pass')
pyclone.remove('drive')

pyclone.ls('drive')
pyclone.copy(src, dest)
pyclone.move(src, dest)

# Do anything else, pass arguments h2cs returns byte string
 result =  pyclone.cmd('-x https://edgeserver -i dirs.txt http://localhost/', 'driver')
 print(result)
```


```python
pipenv install pyclone
```

# Developing pyclone 

To install pyclone, along with all the tools you need to develop and run tests, run the following in your virtualenv:

```bash
$ pip install -e .[dev]
```

Drop some feedback, bugs, and feature requests if you can.
