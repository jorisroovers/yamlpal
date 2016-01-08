# yamlpal
[![Build Status](https://travis-ci.org/jorisroovers/yamlpal.svg?branch=master)]
(https://travis-ci.org/jorisroovers/yamlpal)

Simple tool for inserting new entries in yaml files while keeping the original structure and formatting.

Basic usage:
```bash
$ yamlpal insert "invoice" "newkey: newval" examples/sample1.yml

$ yamlpal insert "tax" "newkey: newval" examples/sample1.yml

$ yamlpal insert "bill-to/given" "rhel-7-server" examples/sample1.yml

$ yamlpal insert "product[1]/sku" "newkey: newvalue" examples/sample1.yml

$ yamlpal insert "bill-to/address/city" "newkey: value" examples/sample1.yml

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