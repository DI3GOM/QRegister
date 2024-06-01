from importlib.resources import path
import numpy as np
import stackk
from masking_patterns import masking_patterns
from files_read import file_read
import draw_square
from generator import QRCodeBIT


class QRimage():
    def __init__(self, message: str, direction: str) -> None:
        qrclass = QRCodeBIT(message)
        self.bit_string = qrclass.bitstring()
        self.qr_array = np.zeros((21, 21))
        self.stack = stackk.stack(self.bit_string)
        self.direction = direction
    
    def main(self):

        self.put_data_on_code()
        masking_qr_class = masking_patterns(self.qr_array)
        self.qr_masked_num = masking_qr_class.main()
        self.qr_array = self.format_information_putting()
        
        draw_square.generate_image(data=self.qr_array, path= self.direction)
        

    def format_information_putting(self):
        # files read class
        fileRead = file_read()
        fis_dict = fileRead.format_information()
        fis = fis_dict[self.qr_masked_num[1]]

        # put the striing into a stack
        fis1_stack = stackk.stack(fis)
        fis2_stack = stackk.stack(fis)


        # qr in local variable
        qr = self.qr_masked_num[0]

        # add the first stack the one on square

        for i in range(6):
            qr[8][i] = int(fis1_stack.pop())
        
        qr[8][7] = int(fis1_stack.pop())
        qr[8][8] = int(fis1_stack.pop())
        qr[7][8] = int(fis1_stack.pop())

        for i in range(6):
            qr[5 - i][8] = int(fis1_stack.pop())
        
        # add the second stack on the square
        for i in range(7):
            qr[20 - i][8] = int(fis2_stack.pop())
        
        for i in range(8):
            qr[8][13 + i] = int(fis2_stack.pop())
        
        return qr

    
    def patterns(self):
        starting_squares = [(0,0), (0,14), (14, 0)]
        smaller_square = [(2,2), (2,16), (16, 2)]
        # Alignment patterns
        for i in starting_squares:
            for j in range(i[0], i[0] + 7):
                self.qr_array[j][i[1]] = 1

            for j in range(i[0], i[0] + 7):
                self.qr_array[j][i[1] + 6] = 1

            for j in range(i[1], i[1] + 7):
                self.qr_array[i[0]][j] = 1

            for j in range(i[1], i[1] + 7):
                self.qr_array[i[0] + 6][j] = 1
        
        for i in smaller_square:
            for j in range(i[0], i[0] + 3):
                for k in range(i[1], i[1] + 3):
                    self.qr_array[j][k] = 1

        # timing patterns
        for i in range(8, 14):
            if i%2 == 0:
                self.qr_array[6][i] = 1
                self.qr_array[i][6] = 1
        
        # dark module
        self.qr_array[13][8] = 1

        
    def put_data_on_code(self):
            #the first three squares
        self.patterns()
        self.zigzag_up((20, 20), 24)
        self.zigzag_down((9, 18), 24)
        self.zigzag_up((20, 16), 24)
        self.zigzag_down((9, 14), 24)
        self.zigzag_up((20, 12), 40)
        self.zigzag_down((0, 10), 40)
        self.zigzag_up((12, 8), 8)
        self.zigzag_down((9, 5), 8)
        self.zigzag_up((12, 3), 8)
        self.zigzag_down((9, 1), 8)



    def zigzag_up(self, starting_pos: tuple, len_num):
        starting_bit = 0
        height = 0
        for i in range(1, len_num + 1):
            bit = self.stack.pop()
        
            if starting_bit < 1:
                self.qr_array[starting_pos[0]][starting_pos[1]] = bit
                starting_bit += 1

            elif i%2 == 0:
                if starting_pos[0] - height == 6:
                    height += 1
                    self.qr_array[starting_pos[0] - height][starting_pos[1] - 1] = bit
                    height += 1

                else:
                    self.qr_array[starting_pos[0] - height][starting_pos[1] - 1] = bit
                    height += 1


            elif i%2 != 0:
                if starting_pos[0] - height == 6:
                    height += 1
                    self.qr_array[starting_pos[0] - height][starting_pos[1] - 1] = bit

                else:
                    self.qr_array[starting_pos[0] - height][starting_pos[1]] = bit

            
    
        
    def zigzag_down(self, starting_pos: tuple, len_num):
        starting_bit = 0
        height = 0
        for i in range(1, len_num + 1):
            bit = self.stack.pop()
            if starting_bit < 1:
                self.qr_array[starting_pos[0]][starting_pos[1]] = bit
                starting_bit += 1

            elif i%2 == 0:
                if starting_pos[0] + height == 6:
                    height += 1
                    self.qr_array[starting_pos[0] + height][starting_pos[1] - 1] = bit
                    height += 1
                else:
                    self.qr_array[starting_pos[0] + height][starting_pos[1] - 1] = bit
                    height += 1


            elif i%2 != 0:
                if starting_pos[0] + height == 6:
                    height += 1
                    self.qr_array[starting_pos[0] + height][starting_pos[1]] = bit

                else:
                    self.qr_array[starting_pos[0] + height][starting_pos[1]] = bit

            


        
if __name__ == '__main__':
    a = QRimage('QRegister', direction='C:/Users/yeyom/OneDrive/Escritorio/QR code generator/Actual generator/images/regis,jpeg')
    a.main()


