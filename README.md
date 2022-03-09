# gitlike-commands

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![GitHub stars](https://img.shields.io/github/stars/unixorn/gitlike-commands.svg)](https://github.com/unixorn/gitlike-commands/stargazers)
[![Issue Count](https://codeclimate.com/github/unixorn/gitlike-commands/badges/issue_count.svg)](https://codeclimate.com/github/unixorn/gitlike-commands)

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

```toml
[tool.poetry.scripts]
gitalike-demo = "gitlike_commands:subcommand_driver"
```