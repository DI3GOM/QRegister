class bit_wise_operations():
    def __init__(self, decimal1, decimal2) -> None:
        self.byte1 = bin(decimal1)[2:]
        self.byte2 = bin(decimal2)[2:]

        if len(self.byte1) != len(self.byte2):
            bigger_num = max(len(self.byte1), len(self.byte2))
            smaller_num = min(len(self.byte1), len(self.byte2))
            diff = bigger_num - smaller_num
            self.byte1 = '0'*diff + self.byte1 if len(self.byte1) < len(self.byte2) else self.byte1
            self.byte2 = '0'*diff + self.byte2 if len(self.byte2) < len(self.byte1) else self.byte2
            
    
    def exclusive_or(self) -> int:
        # convert into lists for easier manipulation
        bin_list1 = [int(i) for i in list(self.byte1)]
        bin_list2 = [int(i) for i in list(self.byte2)]

        to_ret = int(''.join([str(_a ^ _b) for _a, _b in zip(bin_list1, bin_list2)]), 2)
        return to_ret


            
