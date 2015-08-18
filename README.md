Natural Duration Field
======================
Expose a duration value to your staff and users in a non-hideous
manner. Allows you to accept input such as "3 days and 2 minutes"
or even "6years,32 min & 503ms", and optionally renders values
to the user in a similar manner. 

Requirements
------------
 - Django 1.8 (the first one with a duration field)
 - Python 2.7, 3.4, or PyPy (should work with 3.3, but I haven't tested it)

Usage
-----
Insert a `NaturalDurationField` into a form somewhere. The `human_values` kwarg  tells whether
to render initial values in a nice, humanized fashion (2 days and 30 minutes) or the usual 
django fashion (2 00:30:00). At no point is precision lost when resaved.

Other Notes
-----------
Copyright Jake Merdich, 2015, released under New BSD license.

Largely inspired by the [Juration](https://github.com/domchristie/juration) javascript library.
