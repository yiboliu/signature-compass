# signature-compass
This project mainly provides a python API to query the event signatures and function signatures in the 4bytes.directory's database to get the human-readable representation. 

The server is deployed on digital ocean platform with a url of https://signature-compass-63lof.ondigitalocean.app/.

Currently supported API's include:
1. `get-text-signature`: enter a signature of hex format, it will return the text format, human-readable format of that signature, if it shows up in 4bytes' database. 
Example usage: `curl -X GET "https://signature-compass-63lof.ondigitalocean.app/get-text-signature?hex=0x31a6bf0b"`
2. `list-signature`: enter a text signature and it will retrieve all the information associated with it in 4byte's database. 
A significant feature is that this API supports regex. It supports case-sensitive and insensitive regexes of startswith, endswith and contains. By default, exact match is used. 
Example usage: `curl -X GET "https://signature-compass-63lof.ondigitalocean.app/list-signature?text=<some signature>&exact=false&case_sensitive=True"`
3. `submit-signature`: enter a text signature and it will submit it to 4byte's database. A boolean value of True will be returned if submission is successful and False otherwise.
Example usage: `curl -X POST "https://signature-compass-63lof.ondigitalocean.app/submit-signature?signature=<some signature>"`

Another part of this service is it provides a JavaScript library to interact with it. 
NPM link: https://www.npmjs.com/package/signature-compass-http-client-library.
Please be noted that currently only get-text-signature is supported in the JavaScript Library.

The service is also deployed on fleek, with IPFS hash of `Qme1DA277ADDKGuK1m4Va8wdhte73SULK3ha1JbpYXLFpw`
URL: https://white-block-0229.on.fleek.co/
