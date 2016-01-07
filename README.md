# yamlpal
Simple tool for inserting new entries in yaml files while keeping the original structure and formatting.


Basic usage:
```bash

$ yamlpal "foo/bar/haha" "newkey: newval\n" /path/to/file

# More options:
$ yamlpal --help
Usage: yamlpal [OPTIONS] NEEDLE NEWTEXT FILE

  Simple tool for inserting new entries in yaml files while keeping the
  original structure and formatting

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.
```


## TODO ##

- Check that input file is a valid yaml file
- Tests
- Code cleanup
- Read file names from standard input
- File input using @ syntax
- Better examples/docs