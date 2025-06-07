# SC RPI Client

Python library based on [wled](https://pypi.org/project/wled/) that provides a Python client for [sc-rpi](https://github.com/brunopk/sc-rpi).

As in WLED, the way to use SC RPI Client is with an async context manager :

```python
async with ScRpi("http://localhost:8080/ws") as sc_rpi:
  await sc_rpi.do_something()
```

The base structure for this project was created with Poetry :

```bash
poetry new sc-rpi-client
```

## Development

### Required tools for development

- Poetry

### Recommended extensions for Visual Code

- [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- [Black FormatterPreview](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
- [autoDocstring - Python Docstring Generator](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring)

### Steps to start coding

1. [Create a virtual environment](doc/virtual_environments.md#creating-virtual-environments)
2. [Activate the virtual environment](doc/virtual_environments.md#activating-the-environment)
3. Install dependencies with Poetry
4. Start coding!

## Links

- [mashumaro](https://pypi.org/project/mashumaro/)
