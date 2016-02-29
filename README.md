# yamlpal
[![Build Status](https://travis-ci.org/jorisroovers/yamlpal.svg?branch=master)]
(https://travis-ci.org/jorisroovers/yamlpal)

Simple tool for inserting new entries in yaml files while keeping the original structure and formatting.

Basic usage:
```bash
$ yamlpal insert -f examples/sample1.yml "invoice" "newkey: newval"

$ yamlpal insert -f examples/sample1.yml "tax" "newkey: newval"

$ yamlpal insert -f examples/sample1.yml"bill-to/given" "rhel-7-server"

$ yamlpal insert  -f examples/sample1.yml "product[1]/sku" "newkey: newvalue"

$ yamlpal insert  -f examples/sample1.yml "bill-to/address/city" "newkey: value"

# Specify files via stdin:
$ find examples -name \*.yml | yamlpal insert "invoice" "newkey: value"

# More options:
$ yamlpal --help
Usage: yamlpal [OPTIONS] COMMAND [ARGS]...

  Modify yaml files while keeping the original structure and formatting.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  insert  Insert new content into a yaml file.
```


## Wishlist ##

We maintain a [wishlist on our wiki](https://github.com/jorisroovers/yamlpal/wiki/Wishlist).