# SC RPI Client

Python library based on [wled](https://pypi.org/project/wled/) that provides a client for [sc-rpi](https://github.com/brunopk/sc-rpi). As in WLED, the way to use SC RPI Client is with an async context manager :

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

- [Poetry](doc/poetry.md)

### Recommended extensions for Visual Code

- [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- [Black FormatterPreview](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
- [autoDocstring - Python Docstring Generator](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring)
