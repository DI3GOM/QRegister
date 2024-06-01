import numpy as np
from files_read import file_read
from error_correction import polynomial_div

class QRCodeBIT():
    def __init__(self, word) -> None:
        self.word = word

    def alphanumeric_encoding(self):
        # Attach the length and mode indicator at the beggining
        word = self.word
        mode_indicator='0010'
        number_max_databytes = 16
        number_max_databits = 8*number_max_databytes

        # finding the length of the binary
        length_word_bin = bin(len(word))[2:]
        while len(length_word_bin) < 9:
                    length_word_bin = '0' + length_word_bin

        # alphanumeric only uses uppercase letters
        letters = list(word.upper())
        
        # Import the alphanumeric dictionary of values
        fr = file_read()
        list_char = fr.alphanum_value(letters)
        two_chars = [list_char[x:x+2] for x in range(0, len(list_char), 2)]
        binary_individual_string = [mode_indicator, length_word_bin]

        # convert into a binary string and append to the final
        for i in two_chars:
            if len(i)%2 == 0:
                sequence = bin(int(i[0])*45 + int(i[1]))[2:]
                while len(sequence) < 11:
                    sequence = '0' + sequence
                
                binary_individual_string.append(sequence)
            else:
                sequence = bin(int(i[0]))[2:]
                while len(sequence) < 6:
                    sequence = '0' + sequence

                binary_individual_string.append(sequence)


        #Adding the terminator bits
        bit_string = ''
        for i in binary_individual_string:
            bit_string = bit_string + i
        
        

        if number_max_databits - len(bit_string) >= 4:
            bit_string = bit_string + '0'*4
        else: 
            bit_string = bit_string + '0'*(number_max_databits - len(bit_string))
        
        
        # completing with 0 until len mod 8 = 0
        mod8 = len(bit_string) % 8
        
        if mod8 != 0:
            bit_string = bit_string +  ('0'*(8 - mod8))


        # creating a list with all of the bytes
        list_8bits = [bit_string[x:x+8] for x in range(0, len(bit_string), 8)]

        if len(list_8bits) > 16:
            return ['Word too big']

        # Completing with extra bytes 276 and 17 if it is too short
        extra_bytes = ['11101100', '00010001']
        for i in range(number_max_databytes - len(list_8bits)):
            extra = extra_bytes[i % 2]
            list_8bits.append(extra)



        return list_8bits

    def byte_encoding(self):
        # Attach the length and mode indicator at the beggining
        word = self.word
        mode_indicator='0100'
        number_max_databytes = 16
        number_max_databits = 8*number_max_databytes

        # finding the length of the binary
        length_word_bin = bin(len(word))[2:]
        length_word_bin = length_word_bin.zfill(8)

        # turn the word into a list
        letters = list(word)
        
        # Import the alphanumeric dictionary of values
        fr = file_read()
        list_char = fr.byte_value(letters)
        binary_individual_string = [mode_indicator, length_word_bin]

        # convert into a binary string and append to the final
        for i in list_char:
            binary_individual_string.append(i)



        #Adding the terminator bits
        bit_string = ''
        for i in binary_individual_string:
            bit_string = bit_string + i
        
        

        if number_max_databits - len(bit_string) >= 4:
            bit_string = bit_string + '0'*4
        else: 
            bit_string = bit_string + '0'*(number_max_databits - len(bit_string))
        
        
        # completing with 0 until len mod 8 = 0
        mod8 = len(bit_string) % 8
        
        if mod8 != 0:
            bit_string = bit_string +  ('0'*(8 - mod8))


        # creating a list with all of the bytes
        list_8bits = [bit_string[x:x+8] for x in range(0, len(bit_string), 8)]

        if len(list_8bits) > 16:
            return ['Word too big']

        # Completing with extra bytes 276 and 17 if it is too short
        extra_bytes = ['11101100', '00010001']
        for i in range(number_max_databytes - len(list_8bits)):
            extra = extra_bytes[i % 2]
            list_8bits.append(extra)

        bruh = ''
        for i in list_8bits:
            bruh += i


        return list_8bits
    
    def bitstring(self):
        w = self.byte_encoding()

        e= polynomial_div(w)
        error_word = e.division()

        final = ''
        for i in w:
            a = bin(i)[2:]
            a = a.zfill(8)

            final += a
        
        for j in error_word:
            final += j
        
        return final








if __name__ == '__main__':
    binary = '00100000 01011011 00001011 01111000 11010001 01110010 11011100 01001101 01000011 01000000 11101100 00010001 11101100'.replace(' ', '')
    e = QRCodeBIT('ñucu')
    answer = e.byte_encoding()
    mari = '01000000011101100111011001010110111001100101011100110110100101110011000011101100000100011110110000010001111011000001000111101100'

    


   # AC-42
