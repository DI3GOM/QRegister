from bitwise_op import bit_wise_operations
import copy



class polynomial_div ():
    def __init__(self, coefficients: list) -> None:
        
        # generate alpha values table to convert
        self.exponents_alpha = []
        self.integers = []

        for i in range(256):
            self.exponents_alpha.append(i)
            self.integers.append(self.alpha_exponents(i, 1))


        # transform the binary message to integers
        self.list_ret = []
        for i in range(len(coefficients)):
            coefficients[i] = int(coefficients[i], 2)
        
        # create the message polynomial
        self.message_poly = [['int', coefficients[i - 1], 'x', len(coefficients) - i] for i in range(1, len(coefficients) + 1)]
            

        # create the generator polynomial
        self.generator_poly = [['alpha', 0, 'x', 10],['alpha', 251, 'x', 9],['alpha', 67, 'x', 8],['alpha', 46, 'x', 7],['alpha', 61, 'x', 6],['alpha', 118, 'x', 5],['alpha', 70, 'x', 4],['alpha', 64, 'x', 3],['alpha', 94, 'x', 2],['alpha', 32, 'x', 1],['alpha', 45, 'x', 0]]
        


    
    def switch_mode(self, list):
        if list[0][0] == 'alpha':
            for i in range(len(list)):
                list[i][0] = 'int'
                list[i][1] = self.integers[self.exponents_alpha.index(list[i][1])]

        return list

    def alpha_exponents(self, exponent, decimal):

        if exponent == 1:
            return ( decimal*2) if decimal*2 <= 255 else ( bit_wise_operations(decimal*2, 285).exclusive_or())
        
        elif exponent == 0:
            return 1
        
        elif decimal*2 <= 255:
            return self.alpha_exponents(exponent - 1, decimal*2)

        elif decimal*2 > 255:
            return self.alpha_exponents(exponent - 1, bit_wise_operations(decimal*2, 285).exclusive_or())

    def division (self):
        # multiply the x exponents by n, where n is the number of error correction words necessary, in 1-m it is 10
        # the result is in integer mode while the generator polynomial is in alpha mode
        result = self.message_poly
        for i in range(len(result)):
            result[i][3] += 10
        
        # Begin division polinomial first step
        while len(result) >= len(self.generator_poly):
            temporary_result = []
            temporary_generator = copy.deepcopy(self.generator_poly)


            # multiply the alpha exponents in order to generate the final polynomial
            alpha_exponent_to_add = self.exponents_alpha[self.integers.index(result[0][1])]


            for i in range(len(temporary_generator)):
                temporary_generator[i][1] += alpha_exponent_to_add
                
                if temporary_generator[i][1] > 255: temporary_generator[i][1] = temporary_generator[i][1] % 255

            # using XOR for the integers
            temporary_generator =  self.switch_mode(temporary_generator)
            for i in range(len(temporary_generator)):
                number = temporary_generator[i][1] ^ result[i][1]
                temporary_result.append(['int', number, 'x', result[i][3]])

            point_not_xored = len(temporary_generator)

            for i in result[point_not_xored:]:
                temporary_result.append(i)
            
            while temporary_result[0][1] == 0:
                temporary_result.pop(0)
            
            

            result = temporary_result



        while result[-1][3] != 0:
            temporary_result = []
            temporary_generator = copy.deepcopy(self.generator_poly)

        # multiply the x terms of the generator polynomial so they are the same as the message polynomial
            diff = result[0][3] - temporary_generator[0][3]
            for i in range(len(temporary_generator)):
                temporary_generator[i][3] += diff

        # generating the alpha exponent to add
            alpha_exponent_to_add = self.exponents_alpha[self.integers.index(result[0][1])]
            for i in range(len(temporary_generator)):
                    temporary_generator[i][1] += alpha_exponent_to_add
                    if temporary_generator[i][1] > 255: temporary_generator[i][1] = temporary_generator[i][1] % 255

        # creating the temporary result
            temporary_generator =  self.switch_mode(temporary_generator)
            for i in range(len(result)):
                number = temporary_generator[i][1] ^ result[i][1]
                temporary_result.append(['int', number, 'x', result[i][3]])
            

            temporary_result.pop(0)
            temporary_result.append(temporary_generator[-1])
            result = temporary_result


        result_coe = []
        re = []
        for i in result:
            byte = bin(i[1])[2:]
            re.append(byte)
            if len(byte) < 8:
                while len(byte) < 8:
                    byte = '0' + byte

            result_coe.append(byte)
            

        return result_coe
        



if __name__ == '__main__':
    pass
    