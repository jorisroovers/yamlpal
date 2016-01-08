# yamlpal
[![Build Status](https://travis-ci.org/jorisroovers/yamlpal.svg?branch=master)]
(https://travis-ci.org/jorisroovers/yamlpal)

Simple tool for inserting new entries in yaml files while keeping the original structure and formatting.

Basic usage:
```bash
$ yamlpal "invoice" "newkey: newval\n" examples/sample1.yml

$ yamlpal "tax" "newkey: newval\n" examples/sample1.yml

$ yamlpal "bill-to/given" "rhel-7-server\n" examples/sample1.yml

$ yamlpal "product[1]/sku" "newkey: newvalue\n" examples/sample1.yml

$ yamlpal "bill-to/address/city" "newkey: value\n" examples/sample1.yml

# More options:
$ yamlpal --help
Usage: yamlpal [OPTIONS] NEEDLE NEWTEXT FILE

  Simple tool for inserting new entries in yaml files while keeping the
  original structure and formatting

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.
```


## Wishlist ##

We maintain a [wishlist on our wiki](https://github.com/jorisroovers/yamlpal/wiki/Wishlist).