# Natural Duration Field
Expose a duration value to your staff and users in a non-hideous
manner. Allows you to accept input such as "3 days and 2 minutes"
or even "6years,32 min & 503ms", and optionally renders values
to the user in a similar manner. 

## Requirements
 - Django 1.8 (the first one with a duration field)
 - Python 2.7, 3.4, or PyPy (should work with 3.3, but I haven't tested it)

## Usage
1. Add `natural_duration` to your INSTALLED\_APPS
2. Insert a field into a form somewhere

## Other Notes
(c) Jake Merdich, 2015, released under New BSD license.

Largely inspired by the [Juration](https://github.com/domchristie/juration) javascript library.
