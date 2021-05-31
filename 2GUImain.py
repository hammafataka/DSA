import hashlib
import os
import random
import re
import sys
import time
from pathlib import Path

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QLineEdit, QDialog, QGroupBox, \
    QGridLayout, QVBoxLayout, QWidget, QMessageBox


def show_new_window():
    global w
    w = Receiver()
    w.show()
    return w


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.horizontalGroupBox = QGroupBox()
        self.title = 'QtPY DSA'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 100
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGridLayout()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)

        self.show()

    def createGridLayout(self):
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)

        Browse_label = QLabel("select a file")
        Browse_Entry = QLineEdit()
        Browse_Entry.setMinimumWidth(300)
        File_name_label = QLabel("File name:")
        File_Type_label = QLabel("Type:")
        File_location_Label = QLabel("Location")
        File_Size_Label = QLabel("Size:")
        File_Created_Label = QLabel("Created:")
        File_Modified_Label = QLabel("Modified:")

        def gcd(a, b):
            while b != 0:
                a, b = b, a % b
            return a

        def Hash(string):
            hash_sha3_512 = hashlib.new("sha3_512", string.encode())
            hashed = open('C:\\Users\hamma\\OneDrive\\Desktop\\RSA\\hashed.txt', 'w')
            s = hash_sha3_512.hexdigest()
            hashed.writelines(s)
            hashed.close()
            return s

        def Get_file_Content(filetype):
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, filetype, QtCore.QDir.rootPath(), '*')
            File = open(fileName, 'r')
            FILE_content = File.read()
            Text = FILE_content
            return Text

        def load_key():
            public_file = Get_file_Content('public file')
            private_file = Get_file_Content('private file')
            private_Key_Entry.setText(private_file)
            public_Key_Entry.setText(public_file)

        def Save_keys():
            public_text = public_Key_Entry.text()
            private_text = private_Key_Entry.text()
            publicFile = open('C:\\Users\hamma\\OneDrive\\Desktop\\RSA\\public.txt', 'w')
            publicFile.writelines(public_text)
            publicFile.close()

            privateFile = open('C:\\Users\hamma\\OneDrive\\Desktop\\RSA\\Private.txt', 'w')
            privateFile.writelines(private_text)
            privateFile.close()

        def browsefile():
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath(), '*')
            File = open(fileName, 'r')
            FILE_content = File.read()
            Text = FILE_content
            Browse_Entry.setText(fileName)
            split_tup = os.path.splitext(fileName)
            file_extension = split_tup[1]
            FileName = Path(fileName).stem
            FileSize = Path(fileName).stat().st_size
            Modified = os.path.getmtime(fileName)
            ModifiedDate = ("Date modified: " + time.ctime(Modified))
            Created = os.path.getctime(fileName)
            CreatedDate = ("Date created: " + time.ctime(Created))
            File_name_label.setText("Name: " + FileName)
            File_Type_label.setText("Type: " + file_extension)
            File_location_Label.setText("Location: " + fileName)
            File_Size_Label.setText("size: " + FileSize.__str__() + " byte")
            File_Created_Label.setText(CreatedDate)
            File_Modified_Label.setText(ModifiedDate)
            return Text

        def MultiInverse(e, phi):
            d = 0
            x1 = 0
            x2 = 1
            y1 = 1
            temp_phi = phi
            while e > 0:
                temp1 = temp_phi // e
                temp2 = temp_phi - temp1 * e
                temp_phi = e
                e = temp2
                x = x2 - temp1 * x1
                y = d - temp1 * y1
                x2 = x1
                x1 = x
                d = y1
                y1 = y
            if temp_phi == 1:
                return d + phi

        def is_prime(num):
            if num == 2:
                return 0
            elif (num < 2) or ((num % 2) == 0):
                return 1
            elif num > 2:
                for i in range(2, num):
                    if not (num % i):
                        return 1
            return 0

        def random_keys():

            p = random.randint(10000000, 90000000)
            while is_prime(p):
                p = random.randint(10000000, 90000000)
            q = random.randint(10000000, 90000000)
            while is_prime(q):
                q = random.randint(10000000, 90000000)
            n = p * q
            phi = (p - 1) * (q - 1)

            e = random.randint(10000000, 900000000)
            while is_prime(e) and not e % phi == 0:
                e = random.randint(10000000, 90000000)

            g = gcd(e, phi)
            while g != 1:
                e = random.randrange(1, phi)
                g = gcd(e, phi)

            d = MultiInverse(e, phi)
            publicFile = open('C:\\Users\hamma\\OneDrive\\Desktop\\RSA\\public.txt', 'w')
            s = "[" + e.__str__() + "," + n.__str__() + "]"
            publicFile.writelines(s)
            publicFile.close()

            privateFile = open('C:\\Users\hamma\\OneDrive\\Desktop\\RSA\\Private.txt', 'w')
            s = "[" + d.__str__() + "," + n.__str__() + "]"
            privateFile.writelines(s)
            privateFile.close()
            publickey = [e, n]
            privatekey = [d, n]
            public_Key_Entry.setText(publickey.__str__())
            private_Key_Entry.setText(privatekey.__str__())
            return (e, n), (d, n)

        def Encrypt(plaintext):
            key, n = re.findall(r'\d+', private_Key_Entry.text())
            cipher = [pow(ord(char), int(key), int(n)) for char in plaintext]
            return cipher

        def Encrypting():
            filename = Browse_Entry.text()
            File = open(filename, 'r')
            FILEcontent = File.read()
            hashed = Hash(FILEcontent)
            encrypted = Encrypt(hashed.__str__())
            Signed_File = open('C:\\Users\hamma\\OneDrive\\Desktop\\RSA\\SignedFile.txt', 'w')
            Signed_File.writelines(encrypted.__str__())
            Signed_File.close()
            QMessageBox.about(self,"Success Encrypting","The Output has been saved in the folder")


        public_Key_Entry = QLineEdit()
        public_Key_Entry.setMinimumHeight(50)
        private_Key_Entry = QLineEdit()
        private_Key_Entry.setMinimumHeight(50)
        public_key_label = QLabel("Enter values for Public key [n1,n2]")
        private_key_label = QLabel("Enter values for private key [n1,n2]")
        Browse_Button = QPushButton("Browse")
        Browse_Button.clicked.connect(browsefile)
        receiver_Button = QPushButton("Receiver Window")
        receiver_Button.clicked.connect(show_new_window)
        receiver_Button.setMinimumWidth(110)
        enc = QPushButton("Sign file")
        enc.setMinimumWidth(150)
        enc.clicked.connect(Encrypting)
        gen = QPushButton('Random values')
        gen.clicked.connect(random_keys)
        gen.setMinimumWidth(150)
        load_Button = QPushButton("Load Keys")
        load_Button.clicked.connect(load_key)
        load_Button.setMinimumWidth(100)
        save_Button = QPushButton("Save Keys")
        save_Button.clicked.connect(Save_keys)
        save_Button.setMinimumWidth(100)
        layout.addWidget(Browse_label, 0, 0)
        layout.addWidget(Browse_Button, 1, 1)
        layout.addWidget(Browse_Entry, 1, 0)
        layout.addWidget(File_name_label, 2, 0)
        layout.addWidget(File_Type_label, 3, 0)
        layout.addWidget(File_location_Label, 4, 0)
        layout.addWidget(File_Size_Label, 5, 0)
        layout.addWidget(File_Created_Label, 6, 0)
        layout.addWidget(File_Modified_Label, 7, 0)
        layout.addWidget(public_key_label, 8, 0)
        layout.addWidget(public_Key_Entry, 8, 1)
        layout.addWidget(load_Button, 8, 2)
        layout.addWidget(private_key_label, 9, 0)
        layout.addWidget(private_Key_Entry, 9, 1)
        layout.addWidget(save_Button, 9, 2)
        layout.addWidget(enc, 10, 0)
        layout.addWidget(gen, 10, 1)
        layout.addWidget(receiver_Button, 10, 2)
        self.horizontalGroupBox.setLayout(layout)


class Receiver(QDialog):
    def __init__(self):
        super().__init__()
        self.horizontalGroupBox = QGroupBox()
        self.title = 'QtPY DSA'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 100
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGridLayout()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)

        self.show()

    def createGridLayout(self):
        def load_key():
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Public file', QtCore.QDir.rootPath(), '*')
            File = open(fileName, 'r')
            FILEcontent = File.read()
            Text = FILEcontent
            Public_Key_Entry.setText(Text)

        def browsefile():
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath(), '*')
            File = open(fileName, 'r')
            FILEcontent = File.read()
            Text = FILEcontent
            Browse_Entry.setText(fileName)
            return Text

        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)
        Browse_Entry = QLineEdit()
        Public_Key_Entry = QLineEdit()
        Public_Key_Entry.setMinimumHeight(60)

        Browse_Entry.setMinimumWidth(300)
        Browse_label = QLabel("Browse a File")
        public_Key_label = QLabel("Enter public key [n1,n2] or load file")

        def Hash():
            File = open(Browse_Entry.text(), 'r')
            FILEcontent = File.read()
            string = FILEcontent
            hash_sha3_512 = hashlib.new("sha3_512", string.encode())
            hash = open('C:\\Users\hamma\\OneDrive\\Desktop\\RSA\\Receiver_hashed.txt', 'w')
            s = hash_sha3_512.hexdigest()
            hash.writelines(s)
            hash.close()
            QMessageBox.about(self,"Success Hash","The Output has been saved in the folder")

        def Decrypt():
            filename = Browse_Entry.text()
            File = open(filename, 'r')
            ciphertext = File.read()
            integer = re.findall(r'\d+', ciphertext)
            for i in range(0, len(integer)):
                integer[i] = int(integer[i])
            ciphertext = integer
            key, n = re.findall(r'\d+', Public_Key_Entry.text())
            aux = [str(pow(char, int(key), int(n))) for char in ciphertext]
            plain = [chr(int(char2)) for char2 in aux]
            decrypted = ''.join(plain)
            receiver_decrypted = open('C:\\Users\hamma\\OneDrive\\Desktop\\RSA\\receiver_decrypted.txt', 'w')
            receiver_decrypted.writelines(decrypted.__str__())
            receiver_decrypted.close()
            QMessageBox.about(self,"Success Decryption","The Output has been saved in the folder")


        Browse_Button = QPushButton("Browse")
        Browse_Button.clicked.connect(browsefile)
        Hash_Button = QPushButton("Hash")
        Hash_Button.clicked.connect(Hash)
        Load_Button = QPushButton("Load")
        Load_Button.clicked.connect(load_key)
        Decryption_Button = QPushButton("Decryption")
        Decryption_Button.clicked.connect(Decrypt)
        layout.addWidget(Browse_label, 0, 0)
        layout.addWidget(Browse_Entry, 1, 0)
        layout.addWidget(Browse_Button, 1, 1)
        layout.addWidget(public_Key_label, 2, 0)
        layout.addWidget(Public_Key_Entry, 2, 1)
        layout.addWidget(Load_Button, 2, 2)
        layout.addWidget(Hash_Button, 3, 2)
        layout.addWidget(Decryption_Button, 3, 0)
        self.horizontalGroupBox.setLayout(layout)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
app = QApplication(sys.argv)
