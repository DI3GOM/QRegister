import math


class masking_test ():
    def __init__(self, list) -> None:
        self.qr = list
        self.penalty_score = 0

    def penalty(self):
        self.adjacent_modules()
        self.squares_same_color()
        self.ident_pattern()
        self.white_black_count()

        return self.penalty_score

    def adjacent_modules(self):
        local_penalty = 0
        # horizontal modules
        for i in self.qr:
            index = 0
            while index < len(i) - 1:

                module_num = 1
                sequence_bit = i[index]
                
                if i[index + 1] == sequence_bit and index < len(i):
                    while index + 1 < len(i) and i[index + 1] == sequence_bit:
                        module_num += 1
                        index += 1

                
                index += 1
        
                if module_num >=5:
                    local_penalty += (3 + module_num - 5)


        # vertical modules
        for i in range(len(self.qr)):
            index = 0
            while index < len(self.qr) - 1:

                module_num = 1
                sequence_bit = self.qr[index][i]
                
                if self.qr[index + 1][i] == sequence_bit and index < len(self.qr):
                    while index + 1 < len(self.qr) and self.qr[index + 1][i] == sequence_bit:
                        module_num += 1
                        index += 1

                
                index += 1


        
                if module_num >=5:
                    local_penalty += (3 + module_num - 5)
        
        self.penalty_score += local_penalty

    def squares_same_color(self):
        local_penalty = 0
        for i in range(len(self.qr) - 1):
            for j in range(len(self.qr) - 1):
                
                value = self.qr[i][j]

                if self.qr[i][j + 1] == value and self.qr[i + 1][j] == value and self.qr[i + 1][j + 1] == value: #Chec if the module below, right and below-right are the same color
                    local_penalty += 3
        
        self.penalty_score += local_penalty
    
    def ident_pattern(self):
        local_penalty = 0

        pattern1 = '00001011101'
        pattern2 = '10111010000'

        #Horizontal pattern finding
        for i in self.qr:
            row = ''
            row.join(str(bit) for bit in i)

            if pattern1 in row:
                local_penalty += 40

            if pattern2 in row:
                local_penalty += 40
        

        #vertical pattern finding
        for i in range(len(self.qr)):
            column = ''
            for j in range(len(self.qr)):
                column += str(self.qr[j][i])
            
            if pattern1 in column:
                local_penalty += 40

            if pattern2 in column:
                local_penalty += 40

        self.penalty_score += local_penalty
    

    def white_black_count(self):
        local_penalty = 0
        black = 0
        multiple = 5
        
        for i in self.qr:
            for j in i:
                if j == 1:
                    black += 1
        

        percentage = (black/441)*100

        lower_end = multiple * math.floor(percentage/multiple)
        upper_end = lower_end + 5


        diff1 = abs(lower_end - 50)/5
        diff2 = abs(upper_end - 50)/5


        local_penalty += (min(diff1, diff2)*10)

        self.penalty_score += local_penalty


if __name__ == '__main__':
    local_penalty = 0

    qr = [[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0], [1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0], [1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0], [1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0], [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0], [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0], [1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0], [1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0], [1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0], [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0], [1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0], [1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0], [1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0], [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0], [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0]]
    

    '''qr = [[1,1,1,1,1,0,0,0,0,0, 1], [1,1,1,1,1,0,0,0,0,0,1], [1,1,1,1,1,0,0,0,0,0,1], [1,1,1,1,1,0,0,0,0,0,1], [1,1,1,1,1,0,0,0,0,0,1] ]'''

    for i in range(len(qr)):
        index = 0
        while index < len(qr) - 1:

            module_num = 1
            sequence_bit = qr[index][i]
            
            if qr[index + 1][i] == sequence_bit and index < len(qr):
                while index + 1 < len(qr) and qr[index + 1][i] == sequence_bit:
                    module_num += 1
                    index += 1



            
            index += 1


    
            if module_num >=5:
                local_penalty += (3 + module_num - 5)
    
        
