from matplotlib.pyplot import draw
import numpy as numpy
import math
from masking_test_file import masking_test
import copy
import draw_square

class masking_patterns():
    def __init__(self, qr) -> None:
        self.qr = qr

        self.qr_ref = numpy.zeros((21, 21))

    def main(self):
        self.reference_qr() # creates the reference qr code
        qr_0 = self.mask_0() # Creates each of the masking patterns
        qr_1 = self.mask_1()
        qr_2 = self.mask_2()
        qr_3 = self.mask_3()
        qr_4 = self.mask_4()
        qr_5 = self.mask_5()
        qr_6 = self.mask_6()
        qr_7 = self.mask_7()

        masking_list = [[qr_0, '0'], [qr_1, '1'], [qr_2, '2'], [qr_3, '3'], [qr_4, '4'], [qr_5, '5'], [qr_6, '6'], [qr_7, '7']]
        lowest_penalty= 0
        best_masking = ''
        counter = 1

        for i in masking_list:
            masking_test_class = masking_test(i[0])
            penalty = masking_test_class.penalty()

            if counter == 1: 
                lowest_penalty = penalty
                best_masking = i
                counter += 1
            else:
                if penalty < lowest_penalty:
                    lowest_penalty = penalty
                    best_masking = i
        
        return best_masking

    def reference_qr(self):
        starting_squares = [(0,0), (0,13), (13, 0)]
        # fill with 1 every square that won't be data or error modeule, to easily create masking patterns
        # Alignment patterns
        first_time = 0
        for i in starting_squares:
            if first_time == 0:
                for j in range(i[0], i[0] + 9):
                    for k in range(i[1], i[1] + 9):
                        self.qr_ref[j][k] = 1

                first_time += 1

            elif first_time == 1:
                for j in range(i[0], i[0] + 9):
                    for k in range(i[1], i[1] + 8):
                        self.qr_ref[j][k] = 1
                first_time += 1

            elif first_time == 2:
                for j in range(i[0], i[0] + 8):
                    for k in range(i[1], i[1] + 9):
                        self.qr_ref[j][k] = 1
                first_time += 1

        # timing patterns
        for i in range(8, 14):
                self.qr_ref[6][i] = 1
                self.qr_ref[i][6] = 1

    def mask_0(self):
        # (row + column)mod 2 == 0
        # IT WORKS
        qr_0 = copy.deepcopy(self.qr)

        for i in range(len(qr_0)):
            for j in range(len(qr_0)):
                if (i + j)%2 == 0 and self.qr_ref[i][j] != 1:
                    qr_0[i][j] = 1 if qr_0[i][j] == 0 else 0
        
        return(qr_0)

    def mask_1(self):
        # 	(row) mod 2 == 0
        # IT WORKS
        qr_1 = copy.deepcopy(self.qr)

        for i in range(len(qr_1)):
            for j in range(len(qr_1)):
                if (i)%2 == 0 and self.qr_ref[i][j] == 0:
                   qr_1[i][j] = 1 if qr_1[i][j] == 0 else 0
        
        return(qr_1)

    def mask_2(self):
        # (column) mod 3 == 0
        qr_2 = copy.deepcopy(self.qr)

        for i in range(len(qr_2)):
            for j in range(len(qr_2)):
                if (j)%3 == 0 and self.qr_ref[i][j] == 0:
                    qr_2[i][j] = 1 if qr_2[i][j] == 0 else 0
        
        return(qr_2)
    
    def mask_3(self):
        # (row + column) mod 3 == 0
        qr_3 = copy.deepcopy(self.qr)

        for i in range(len(qr_3)):
            for j in range(len(qr_3)):
                if (i + j)%3 == 0 and self.qr_ref[i][j] != 1:
                    qr_3[i][j] = 1 if qr_3[i][j] == 0 else 0
        
        return(qr_3)
    
    def mask_4(self):
        # ( floor(row / 2) + floor(column / 3) ) mod 2
        qr_4 = copy.deepcopy(self.qr)

        for i in range(len(qr_4)):
            for j in range(len(qr_4)):
                if ( math.floor(i / 2) + math.floor(j / 3) )%2 == 0 and self.qr_ref[i][j] != 1:
                    qr_4[i][j] = 1 if qr_4[i][j] == 0 else 0
        
        return(qr_4)
    
    def mask_5(self):
         # 	((row * column) mod 2) + ((row * column) mod 3) == 0
        qr_5 = copy.deepcopy(self.qr)

        for i in range(len(qr_5)):
            for j in range(len(qr_5)):
                if ((i*j)%2 + (i*j)%3) == 0 and self.qr_ref[i][j] != 1:
                    qr_5[i][j] = 1  if qr_5[i][j] == 0 else 0
        
        return(qr_5)
    
    def mask_6(self):
        # ( ((row * column) mod 2) + ((row * column) mod 3) ) mod 2
        qr_6 = copy.deepcopy(self.qr)

        for i in range(len(qr_6)):
            for j in range(len(qr_6)):
                if ((i*j)%2 + (i*j)%3)%2 == 0 and self.qr_ref[i][j] != 1:
                    qr_6[i][j] = 1  if qr_6[i][j] == 0 else 0
        
        return(qr_6)
    
    def mask_7(self):
        # ( ((row + column) mod 2) + ((row * column) mod 3) ) mod 2
        qr_7 = copy.deepcopy(self.qr)

        for i in range(len(qr_7)):
            for j in range(len(qr_7)):
                if (((i + j)%2 + (i*j)%3 ) %2) == 0 and self.qr_ref[i][j] != 1:
                    qr_7[i][j] = 1  if qr_7[i][j] == 0 else 0
        
        return(qr_7)
    

    





            
if __name__ == '__main__':

    '''for i in range(len(qr)):
        for j in range(len(qr)):
            if (i + j)%2 == 0 and qr[i][j] != 1:
                qr[i][j] = 1 if qr[i][j] == 0 else 0''' # mask 0
    
    '''for i in range(len(qr)):
        for j in range(len(qr)):
            if (i)%2 == 0 and qr[i][j] != 1:
                qr[i][j] = 1 if qr[i][j] == 0 else 0''' # mask 1

    '''for i in range(len(qr)):
        for j in range(len(qr)):
            if (j)%3 == 0 and qr[i][j] != 1:
                qr[i][j] = 1 if qr[i][j] == 0 else 0''' # mask 2

    '''for i in range(len(qr)):
        for j in range(len(qr)):
            if (i + j)%3 == 0 and qr[i][j] != 1:
                qr[i][j] = 1 if qr[i][j] == 0 else 0''' # mask 3
    
    '''for i in range(len(qr)):
        for j in range(len(qr)):
            if ( math.floor(i/2) + math.floor(j/3) )%2 == 0 and qr[i][j] != 1:
                qr[i][j] = 1 if qr[i][j] == 0 else 0''' # mask 4
    
    '''for i in range(len(qr)):
        for j in range(len(qr)):
            if ((i*j)%2 + (i*j)%3) == 0 and qr[i][j] != 1:
                qr[i][j] = 1  if qr[i][j] == 0 else 0''' # mask 5
    
    '''for i in range(len(qr)):
        for j in range(len(qr)):
            if ((i*j)%2 + (i*j)%3)%2 == 0 and qr[i][j] != 1:
                qr[i][j] = 1  if qr[i][j] == 0 else 0''' # mask 6

    '''for i in range(len(qr)):
        for j in range(len(qr)):
            if (((i + j)%2 + (i*j)%3 ) %2) == 0 and qr[i][j] != 1:
                qr[i][j] = 1  if qr[i][j] == 0 else 0''' #mask 7

    qr = numpy.zeros((21, 21))
    for i in range(len(qr)):
        for j in range(len(qr)):
            if (j)%3 == 0 and qr[i][j] != 1:
                qr[i][j] = 1 if qr[i][j] == 0 else 0
    
    # draw_square.generate_image(qr)
    









        

