# Virtual environments

## Creating virtual environments

```bash
python3 -m venv .direnv
```

where *.direnv* is the virtual environment directory, or :

```bash
virtualenv -p /usr/bin/python .direnv
```

where */usr/bin/python points* to the Python interpreter.

</br>
</br>

> In order to be automatically detected by Visual Code IDE, create the virtual environment in a folder called *.direnv*

## Activating the environment

```bash
source .direnv/bin/activate
```
