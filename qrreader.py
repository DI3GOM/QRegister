from pyexpat.errors import messages
from pyzbar import pyzbar
import cv2

class qrReader():
    def __init__(self) -> None:
        pass

    def main(self):

        camera = cv2.VideoCapture(0)
        ret, frame = camera.read()
        

        while ret:
            # It starts the camera and shows the frames in a window
            ret, frame = camera.read()
            # Checks each frame for a QR code
            condition, messages = self.read_codes(frame)
            cv2.imshow('Barcode/QR code reader', frame)
            # If 'esc' key is pressed or if a QR is detected it closes the window
            if cv2.waitKey(1) & 0xFF == 27 or condition == True:
                break

        camera.release()
        cv2.destroyAllWindows()
        return messages

    def read_codes(self, frame):

        codes = pyzbar.decode(frame)
        decoded_messages = []
        # decodes the codes in the frames if there are any
        for code in codes:
            code_info = code.data.decode('utf-8')
            decoded_messages.append(code_info)
        
        # If there are codes, then the codes are returned
        if decoded_messages != []:

            return True, decoded_messages
        else:
            return False, decoded_messages

    

if __name__ == '__main__':
    hello = qrReader()
    hello.main()