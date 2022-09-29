# Pyclone

<p align="center">
  <img  height="200px" src="https://i.gyazo.com/895208fd1863d4ab41f61d0bae8fa7c7.png" />
</p>

Rclone for the python environment and your virtual environment. Comes bundled with the Rclone binary so, no need to have Rclone pre-installed.

###            Installation

- The installation automatically downloads the rclone binaries so there is no prerequisite to having rclone prior.
- Run the following to install:
    ```python
    pip install pyclone-module
    ```
    
## Configuration

- ##### If you already have rclone pre-installed and want to use that specific binary you can set the paths using the the `pyclone.set_path() `method:

    ```python
    import pyclone
    pyclone.set_path(path=PATH_TO_RCLONE,config=PATH_TO_CONFIG)
    ```
- ##### If you already have your own rclone.conf and want to use it you can set the paths using the the `pyclone.set_config_path() `method:

    ```python
    import pyclone
    pyclone.set_config_path(config="/path/to/config")
    ```

## Usage

#### CLI

- Pyclone is a wrapper or rclone, so you can use the same commands you regularly use in rclone. Visit rclone.org/commands for further information.

    ```bash
    user:~$ pyclone config
    ```
    
### Import Pyclone into your projects

- Importing pyclone into your projects to have programatic control of *rclone* is as simple as `import pyclone`. Further usage will require some knowlegde on some of the classes.

    ```python
    import pyclone
    pyc = pyclone.Pyclone()
    ```

#### Pyclone classes

There are three major classes in Pyclone:

- pyclone.Pyclone()
- pyclone.RemoteManager()
- pyclone.Remote()

## 1. pyclone.Pyclone()

- This is the main pyclone object that is ressponsible for communicating with the **Rclone** shell. You will be dealing with this class mostly. Instanitate it like this

    ```python
    import pyclone
    pyc = pyclone.Pyclone()
    ```

#### 1.1 pyclone.Pyclone().execute(command)

- Pyclone utilizes the `subprocess` module to communicate with the shell and the `execute` method allows you to send commands directly to rclone. Commands have to are expected to be in **list** format. This returns a **Response** object which contains the **text**, **stdout**, **stderr**, **responsecode** and **args** instance variables. 

    ```python
    >>> import pyclone
    >>> command = ['help']
    >>> pyc = pyclone.Pyclone()
    >>> response = pyc.execute(command)
    >>> print(reponse.responsecode)
    0 
    >>> print(repsponse.text)
    Ommited..
    ...
    ...
    ```

#### 1.2 Create a Remote `pyc.config_create()`

- 
    ```python
    import pyclone
    pyc = pyclone.Pyclone()
    pyc.config_create('remote_type', 'remote_name', 'remote@email.com', 'remote_pass')
    ```

#### 1.3 Delete a remote `pyc.config_delete()`

- 
    ```python
    pyc.config_delete('remote_name')
    ```

#### 1.4 Move/Copy `pyc.copy()/pyc.move()`

- **Note** that the the remote has to be appended by a colon at the end which will end up looking like:
pyc.copy(file.zip, 'remote:')

    ```python
    pyc.copy('src:path', 'dest:path')
    pyc.move('src:path', 'dest:path')
    ```
#### 1.5 List directory (ls) `pyc.copy()/pyc.move()`
- 
    ```python
    pyc.ls('remote:path')
    ```

## Using the Remote Manager and Remote object

### 2 pyclone.RemoteManager()

- The Remote Mangager brings everything together by mangaing your remotes, and extending the functionality of the Pyclone and Remote objects.

    ```python
    >>> import pyclone
    >>> remotes = pyclone.RemoteManager()
    >>> remotes.show()
    ['remote_A', 'remote_B']
    ```

#### 1.2 Create/Deleting a Remote `remotes.create()/remotes.delete()`

- 
    ```python
    remotes.create('remote_type', 'remote_name', 'remote@email.com', 'remote_pass')
    remotes.delete('remote_name')
    ```

### Remote Objects

#### 2.1 Get a Remote `remotes.get_remote()`

- This returns a `Remote` object that inherits most of its functionality from the Pyclone object.

    ```python
    remote_A = remotes.get_remote('remote_A')
    ```

#### 2.2 Remote methods

- `remote.ls()`
- `remote.copy('file', dl=False)`
    - If `dl=True` this will download the file from the remote.
- `remote.move('file:path', dl=False)`
    - If `dl=True` this will download the file from the remote. 
- `remote.delete('file:path')`
- `remote.size()`

### Future:

- Non-blocking subprocesses
- pyclone.Remote.check()

## Developing pyclone

To install pyclone, along with all the tools you need to develop and run tests, run the following in your virtualenv:

```bash
user:~$ pip install -e .[dev]
```

Drop some feedback, bugs, and feature requests if you can.
