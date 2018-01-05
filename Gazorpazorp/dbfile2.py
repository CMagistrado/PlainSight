#!/usr/bin/env python
# From DynamoDB Download, to private_key file
import json, sys

class db2priv:

    def convert(self, dbfile):

        # Opens Database File for Read Access
        dbf = open(dbfile, 'r')

        # Create the output file of privfile
        privf = open("privfile", "w+")

        for line in dbf:
            # Parses json line by line
            parsed_json = json.loads(line)
            string_key = parsed_json['private_key']
            key = string_key['s']
            privf.write(key + "\n")

        # Closes private_key file
        privf.close()
        
        return

if __name__ == "__main__":
    
    d = db2priv()
    dbfile = sys.argv[1]

    # Parses the json and writes it to privfile
    d.convert(dbfile)