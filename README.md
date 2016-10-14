# Easy domain adding
Add a site in just one command. This works only with apache I'm planning to add support for nginx later.

## Usage
To add a domain just type:
````
./addDomain.py -d example.com
````

You can also add a subdomain:
````
./addDomain.py -d example.com -s example
````

Note: If you install it in the folder: **/usr/local/bin** you can call the script global by typing the commands above without ./

## TODO
- Adding https/http2.0 support
- Adding nginx support
- Improve code
- Automatically create a FTP account
