# selgooglevoice

A Selenium with Python replacement for pygooglevoice


Usage:

py gvoice.py google-email google-password phone-number

The phone number must include the country code, which is 1 for USA and Canada, and contain only digits.  For example: 18005551212

It will call from the linked number in your Google Voice account.  It has only been tested with an account with a single linked phone number.

You will need to change lines 14 and 15 to indicate a directory to store cookies, and the path for your chromedriver.

If you prefer to use geckodriver (Firefox), use gvoice-ff.  Place geckodriver (or the Windows geckodriver.exe) in the same directory as gvoice-ff, or in your PATH.
