#!/usr/bin/env python

# importing binascii to be able to convert hexadecimal strings to binary data
import binascii, hashlib, base58, sys

class convert():

    def p2wif(self, key):
    #Takes the a file of private_keys in raw format and convers it to
    # Step 1: here we have the private key
        pk = key

        # Step 2: let's add 80 in front of it
        extended_key = "80"+pk

        # Step 3: first SHA-256
        first_sha256 = hashlib.sha256(binascii.unhexlify(extended_key)).hexdigest()

        # Step 4: second SHA-256
        second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()

        # Step 5-6: add checksum to end of extended key
        final_key = extended_key+second_sha256[:8]
            
        # Step 7: finally the Wallet Import Format is the base 58 encode of final_key
        WIF = base58.b58encode(binascii.unhexlify(final_key))
            
        return WIF

    def open_file(self, file):

        # Creates the file privWIF
        w = open('privWIF', 'w+')

        with open(file) as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            for i in content:
                w.write(self.p2wif(i) + "\n")
        
        w.close()
        return

if __name__ == "__main__":

    privFile = sys.argv[1]
    c = convert()
    c.open_file(privFile)
