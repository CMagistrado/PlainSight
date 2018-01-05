#!/usr/bin/env python
#
#   --------------------------- Logic ---------------------------
#   Highest Possible Ascii Value = 34 * highest_single_ascii_value
#   The subtract_value = ascii_repnumber - total_number_of_possible
#   abs(dbID) =  ascii_repnumber - subtract_value
#   dbID = range(0,total_ascii_repnumber)
#   0. Convert derivative into ascii number
#   1. Take that number subtract that total possible permutations
#   2. result minus total_number_of_possible will give us the DB-ID.
#
#   Testing:
#
#   str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" -- total = 2015
#   subtract 'O' and 'I', which are 79 and 73   = 1863
#
#   str = "abcdefghijklmnopqrstuvwxyz" -- total = 2847
#   subtract 'l', which is 108                  = 2739
#
#   str = '0123456789' ------------------ total = 525
#   subtract acsii value of 0, which is 48      = 477 
#
#   Highest Possible Ascii Value: highest_CAPS_value + highest_lowercase_value + highest_ascii_numberical_value
#   1863 + 2739 + 477                           = 5079
#
#   The Highest Number of Possible characters * Highest Possible Ascii Value will get us 
#   5079 * 32 <-- total char in btc_addr        = 162528

class dbID:

    asciiTotalPossible = 162528
    asciiHighestValue = 5079

    def asciiConv(self, derive):
        
        total = 0

        # Gets a asciivalue to of the derivative
        for i in derive:
            asciiRep = ord(i)
            total += int(asciiRep) 
        return total

    def sub(self, asciiRepTotal):
        # Subtract asciiTotalPossible by asciiRep to get portal number
        subNum = self.asciiTotalPossible - asciiRepTotal
        return subNum

    def get_dbID(self, subNum):
        dbID = abs(subNum - self.asciiHighestValue)
        return dbID
