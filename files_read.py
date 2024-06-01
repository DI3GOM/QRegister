import os

class file_read():
    def __init__(self) -> None:
        pass

    def alphanumerical(self):
        path = self.get_path() + '/alphanumeric.csv'
        with open(path, 'r') as f:
            alphanum = {}
            for line in f: 
                words = line.split(',')
                alphanum[words[0]] = words[1].replace('\n', '')


            
            return alphanum
    
    def byte(self):
        path = self.get_path() + '/bytes.csv'
        with open(path, 'r') as f:
                lines = {}
                for line in f: 

                    words = line.split(' ,')

                    lines[words[0]] = words[1].replace('\n', '')
        
        for i in lines.keys():
            lines[i] = bin(int(lines[i], 16))[2:].zfill(8)

        return lines


    
    def format_information(self):
        path = self.get_path() + '/format_information_strings.csv'
        with open(path, 'r') as f:
            fis= {}
            for line in f: 
                line_values = line.split(',')
                fis[line_values[0]] = line_values[1].replace('\n', '')
        
        return fis
        
    def alphanum_value(self, list: list):
        values = []
        alpha_dict = self.alphanumerical()

        for i in list:
            if i in alpha_dict.keys():
                values.append(alpha_dict.get(i))
            
            else:
                return []

        return values
    
    def byte_value(self, list: list):
        values = []
        byte_dict = self.byte()

        for i in list:
            if i in byte_dict.keys():
                values.append(byte_dict.get(i))

        return values
    
    def get_path(self):
        path = os.path.abspath(os.path.dirname(__file__))
        path_list = path.split('\\')

        path_str = ''
        for i in range(len(path_list)):
            if i == len(path_list) - 1:
                path_str += path_list[i]
            else:
                path_str += path_list[i] + '/'
        
        return path_str




if __name__ == '__main__' :
    f = file_read()
    let = ['A', 'B', '3', '/']
    print(f.format_information())