---
name: vislog
description: "Guide for using the vislog Python library (>=0.2.2) to add visual logging with nested blocks, rulers, indentation, emoji decorators, and more. Use when writing code that uses vislog, or when the user asks how to add structured visual logging."
---

# vislog - Visual Logger for Python

`vislog` enhances Python's standard `logging` module with visual ASCII effects for better readability. It supports nested log blocks, horizontal rulers, indentation, and emoji-based decorators.

- **PyPI**: `pip install vislog>=0.2.2`
- **Requires**: Python 3.10+
- **Docs**: https://vislog.readthedocs.io/

## Public API

Only two names are exported:

```python
from vislog import VisLog, AlignEnum
```

## Quick start

```python
from vislog import VisLog

logger = VisLog(name="my_app")
logger.info("hello world")
```

Output:

```
[User 2024-01-01 12:00:00] | hello world
```

## VisLog constructor

```python
VisLog(
    logger=None,           # pass your own logging.Logger, or None to auto-create
    name=None,             # logger name (used when auto-creating)
    level=logging.INFO,    # logging level
    log_format="[User %(asctime)s] %(message)s",
    datetime_format="%Y-%m-%d %H:%m:%S",
    tab="  ",              # indentation string (2 spaces)
    pipe="| ",             # pipe character for nesting (single char + space)
)
```

## Logging methods

All methods return the formatted string (useful for assertions in tests).

```python
logger.debug(msg, indent=0, tab=None, pipe=None) -> str
logger.info(msg, indent=0, tab=None, pipe=None) -> str
logger.warning(msg, indent=0, tab=None, pipe=None) -> str
logger.error(msg, indent=0, tab=None, pipe=None) -> str
logger.critical(msg, indent=0, tab=None, pipe=None) -> str
```

- `indent`: extra indentation levels on top of current indent
- `tab`: override the tab string for this call
- `pipe`: override the pipe character for this call

## Horizontal ruler

```python
logger.ruler(
    msg,
    char="-",
    align=AlignEnum.left,    # AlignEnum.left / .right / .middle
    length=80,
    left_padding=5,
    right_padding=5,
    corner="+",
    pipe=None,
    func=None,               # override the logging function (e.g. logger._logger.debug)
) -> str
```

Output:

```
[User ...] +----- my section title ------------------------------------------+
```

## Context managers

### `logger.indent(level=1)`

Temporarily increase indentation level.

```python
logger.info("a")
with logger.indent():
    logger.info("b")
    with logger.indent():
        logger.info("c")
logger.info("d")
```

Output:

```
| a
|   b
|     c
| d
```

### `logger.nested(pipe=None)`

Add a nesting level (adds another pipe column).

```python
logger.ruler("section 1")
logger.info("hello 1")
with logger.nested():
    logger.ruler("section 1.1")
    logger.info("hello 1.1")
logger.ruler("section 1")
```

Output:

```
+----- section 1 -------------------------------------------+
| hello 1
| +----- section 1.1 ---------------------------------------+
| | hello 1.1
| +----- section 1.1 ---------------------------------------+
+----- section 1 -------------------------------------------+
```

### `logger.pipe(pipe=None)`

Temporarily change the pipe character.

```python
logger.info("a")
with logger.pipe("*"):
    logger.info("b")
logger.info("c")
```

Output:

```
| a
* b
| c
```

### `logger.disabled(disable=True)`

Temporarily disable all log output. Useful for silencing logs in tests.

```python
with logger.disabled(disable=True):
    logger.info("this won't print")
```

## Decorators

### `logger.pretty_log(...)`

Full-featured decorator that prints ruler at start, error, and end with elapsed time.

```python
@logger.pretty_log(
    start_msg="Start {func_name}()",
    error_msg="Error {func_name}(), elapsed = {elapsed:.2f} sec",
    end_msg="End {func_name}(), elapsed = {elapsed:.2f} sec",
    char="-", align=AlignEnum.left, length=80,
    left_padding=5, right_padding=5, corner="+",
    nest=0,       # nest the function body by N levels
    pipe=None,    # custom pipe char inside the block
)
def my_func():
    logger.info("working ...")
```

Output:

```
+----- Start my_func() ----------------------------------------+
|
| working ...
|
+----- End my_func(), elapsed = 0.12 sec ----------------------+
```

Template variables: `{func_name}` and `{elapsed}` (plus any **kwargs from the decorated function).

### `logger.start_and_end(msg, ...)`

Simplified version of `pretty_log` with emoji support.

```python
@logger.start_and_end(
    msg="My Function",
    start_emoji="🟢",
    error_emoji="🔴",
    end_emoji="🟢",
    pipe="📦",
)
def my_func(name: str):
    logger.info(f"{name} working")

my_func(name="alice")
```

Output:

```
+----- 🕑 🟢 Start 'My Function' --------------------------+
📦
📦 alice working
📦
+----- ⏰ 🟢 End 'My Function', elapsed = 1.01 sec --------+
```

### `logger.emoji_block(msg, emoji)`

Simplest decorator: one emoji for the whole block.

```python
@logger.emoji_block(msg="Deploy app {app_name}", emoji="🚀")
def deploy_app(app_name: str):
    logger.info("working ...")
    logger.info("done")

deploy_app(app_name="my_app")
```

Output:

```
+----- 🕑 🚀 Start 'Deploy app my_app' ----------------------+
🚀
🚀 working ...
🚀 done
🚀
+----- ⏰ ✅ 🚀 End 'Deploy app my_app', elapsed = 1.01 sec -+
```

The `msg` parameter supports `{keyword}` placeholders that are filled from the decorated function's **kwargs.

## Real-world pattern: nested function calls

```python
from vislog import VisLog

logger = VisLog(name="deploy")

@logger.emoji_block(msg="Run tests", emoji="🧪")
def run_tests():
    logger.info("running unit tests ...")
    logger.info("all passed")

@logger.emoji_block(msg="Deploy {env}", emoji="🚀")
def deploy(env: str):
    logger.info(f"deploying to {env}")
    with logger.nested():
        run_tests()
    logger.info("deploy complete")

deploy(env="production")
```

## On/Off control

```python
logger.off()   # disable logging (stores handlers internally)
logger.on()    # re-enable logging (restores handlers)
```

## AlignEnum

```python
from vislog import AlignEnum

AlignEnum.left    # "<"
AlignEnum.right   # ">"
AlignEnum.middle  # "^"
```

Used in `ruler()` and `pretty_log()` to control text alignment within the ruler line.
