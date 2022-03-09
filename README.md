# gitlike-commands

## Background

`gitlike-commands` is a python module for easily creating `git`-style subcommand handling.

Refactored out of [thelogrus](https://github.com/unixorn/thelogrus/) so you don't have to import any modules that aren't part of the Python standard library.

## Usage

`subcommand_driver` automatically figures out what name the script was called as, then looks for subcommands and runs them if found, passing in any command line options.

So if you have a `foo` script in your `$PATH` as shown below

```python
#!/usr/bin/env python3
from gitlike_commands import subcommand_driver

if __name__ == '__main__':
    subcommand_driver()
```

Running `foo bar baz` will look for a `foo-bar-baz` script, and if present in your `$PATH`, run it. If there is no `foo-bar-baz`, it will look for `foo-bar`, and if it finds that, run `foo-bar baz`.

If you're using poetry in your python project, you can add a gitlike driver as a scripts entry:
```
[tool.poetry.scripts]
gitalike-demo = "gitlike_commands:subcommand_driver"
```