from bitwise_op import bit_wise_operations
from generator import QRCodeBIT
import os

def alpha_exponents(exponent, decimal):

    if exponent == 1 :
        return ( decimal*2) if decimal*2 <= 255 else ( bit_wise_operations(decimal*2, 285).exclusive_or())

    elif exponent == 0:
        return 1
        
    elif decimal*2 <= 255:
        return alpha_exponents(exponent - 1, decimal*2)

    elif decimal*2 > 255:
        return alpha_exponents(exponent - 1, bit_wise_operations(decimal*2, 285).exclusive_or())
    


if __name__ == '__main__':
    events = []
    event_name = 'testremoves'
    path = os.path.abspath(os.path.dirname(__file__))
    path_list = path.split('\\')

    path_str = ''
    for i in range(len(path_list)):
        if i == len(path_list) - 1:
            path_str += path_list[i]
        else:
            path_str += path_list[i] + '/'
    
    print(path_str)








