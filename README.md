# yamlpal
[![Build Status](https://travis-ci.org/jorisroovers/yamlpal.svg?branch=master)]
(https://travis-ci.org/jorisroovers/yamlpal)

Simple tool for modifying and searching yaml files **while keeping the original file formatting**.

Yamlpal uses its own version of 'yamlpath', a syntax similar to xpath, to identify elements in a yaml file.


Basic usage:
```bash
# Inserting new content into files (output is printed to stdout by default)
$ yamlpal insert  -f examples/sample1.yml "bill-to/address/city" "newkey: value"
$ yamlpal insert -f examples/sample1.yml "invoice" @examples/insert-multiline.txt

# Specify files via stdin and modify the files directly inline instead of printing to stdout
$ find examples -name \*.yml | yamlpal insert --inline "invoice" "newkey: value"

# Finding content in files
$ yamlpal find  -f examples/sample1.yml "bill-to/address/city"
city: Royal Oak

# Specify a custom output format (run "yamlpal find --help" for details on format strings)
$ yamlpal find -f examples/sample1.yml --format "%{linenr} %{key} %{value}" "bill-to/address/city"
11 city Royal Oak

# Run yamlpal <command> --help for command specific help.
$ yamlpal insert --help
Usage: yamlpal insert [OPTIONS] NEEDLE NEWCONTENT

  Insert new content into a yaml file.

Options:
  -f, --file PATH  File to insert new content in. Can by specified multiple
                   times to modify multiple files. Files are not modified
                   inline by default. You can also provide (additional) file
                   paths via stdin.
  -i, --inline     Edit file inline instead of dumping it to std out.
  --help           Show this message and exit.
```


## Wishlist ##

We maintain a [wishlist on our wiki](https://github.com/jorisroovers/yamlpal/wiki/Wishlist).