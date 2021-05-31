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

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.horizontalGroupBox = QGroupBox()
        self.title = 'DSA'
        self.initailizacomponents()

    def initailizacomponents(self):
        self.setWindowTitle(self.title)
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

        def load_public_key():
            public_file = Get_file_Content('public file')
            public_Key_Entry.setText(public_file)

        def save_p_k():
            public_text = public_Key_Entry.text()
            publicFile = open('C:\\Users\hamma\\OneDrive\\Desktop\\RSA\\public.txt', 'w')
            publicFile.writelines(public_text)
            publicFile.close()

        def load_private_key():
            private_file = Get_file_Content('private file')
            private_Key_Entry.setText(private_file)

        def Save_private_keys():
            private_text = private_Key_Entry.text()
            privateFile = open('C:\\Users\hamma\\OneDrive\\Desktop\\RSA\\Private.txt', 'w')
            privateFile.writelines(private_text)
            privateFile.close()

        def browsefile():
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath(), '*')
            File = open(fileName, 'r')
            FILE_content = File.read()
            Text = FILE_content
            Browse_Entry.setText(fileName)
            return Text

        def set_File_Info():
            fileName=Browse_Entry.text()
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

        def getRandom():
            num = random.randint(100000, 900000)
            while is_prime(num):
                num = random.randint(100000, 900000)
            return num
        def getRandomE(num2):
            num = random.randint(100000, 9000000)
            while is_prime(num) and not num % num2 == 0:
                num = random.randint(100000, 900000)
            return num

        def random_keys():
            p = getRandom()
            q = getRandom()
            n = p * q
            phi = (p - 1) * (q - 1)
            e = getRandomE(phi)
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

        def Receiver_load_key():
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Public file', QtCore.QDir.rootPath(), '*')
            File = open(fileName, 'r')
            FILEcontent = File.read()
            Text = FILEcontent
            Public_Key_Entry.setText(Text)

        def Receiver_browsefile():
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath(), '*')
            File = open(fileName, 'r')
            FILEcontent = File.read()
            Text = FILEcontent
            Browse_Entry.setText(fileName)
            return Text
        def Receiver_Hash():
            File = open(Recevier_Browse_Entry.text(), 'r')
            FILEcontent = File.read()
            string = FILEcontent
            hash_sha3_512 = hashlib.new("sha3_512", string.encode())
            hash = open('C:\\Users\hamma\\OneDrive\\Desktop\\RSA\\Receiver_hashed.txt', 'w')
            s = hash_sha3_512.hexdigest()
            hash.writelines(s)
            hash.close()
            QMessageBox.about(self,"Success Hash","The Output has been saved in the folder")

        def Decrypt():
            filename = Recevier_Browse_Entry.text()
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


        public_Key_Entry = QLineEdit()
        public_Key_Entry.setMinimumHeight(50)
        private_Key_Entry = QLineEdit()
        private_Key_Entry.setMinimumHeight(50)
        public_key_label = QLabel("Enter public key")
        private_key_label = QLabel("Enter private key")
        Browse_Button = QPushButton("Browse")
        Browse_Button.clicked.connect(browsefile)
        receiver_Button = QPushButton("file details")
        receiver_Button.setMinimumWidth(110)
        receiver_Button.clicked.connect(set_File_Info)
        enc = QPushButton("Sign file")
        enc.setMinimumWidth(150)
        enc.clicked.connect(Encrypting)
        gen = QPushButton('Random values')
        gen.clicked.connect(random_keys)
        gen.setMinimumWidth(150)
        load_Public_Button = QPushButton("Load public Keys")
        load_Public_Button.clicked.connect(load_public_key)
        load_Public_Button.setMinimumWidth(100)
        save_Public_Button = QPushButton("Save public Keys")
        save_Public_Button.clicked.connect(save_p_k)
        save_Public_Button.setMinimumWidth(100)
        save_private_Button = QPushButton("Save private Keys")
        save_private_Button.clicked.connect(Save_private_keys)
        save_private_Button.setMinimumWidth(100)
        load_private_Button = QPushButton("Load private Keys")
        load_private_Button.clicked.connect(load_private_key)
        load_private_Button.setMinimumWidth(100)
        Recevier_Browse_Entry = QLineEdit()
        Public_Key_Entry = QLineEdit()
        Public_Key_Entry.setMinimumHeight(60)
        Recevier_Browse_Entry.setMinimumWidth(300)
        Receiver_Browse_label = QLabel("Browse a File")
        public_Key_label = QLabel("Enter public key")
        Receiver_Browse_Button = QPushButton("Browse")
        Receiver_Browse_Button.clicked.connect(Receiver_browsefile)
        Hash_Button = QPushButton("Hash")
        Hash_Button.clicked.connect(Receiver_Hash)
        Load_Button = QPushButton("Load")
        Load_Button.clicked.connect(Receiver_load_key)
        Decryption_Button = QPushButton("Decryption")
        Decryption_Button.clicked.connect(Decrypt)
        layout.addWidget(Browse_label, 0, 0)
        layout.addWidget(Browse_Button, 1, 1)
        layout.addWidget(Browse_Entry, 1, 0)
        layout.addWidget(File_name_label, 2, 0)
        layout.addWidget(receiver_Button, 2, 1)
        layout.addWidget(File_Type_label, 3, 0)
        layout.addWidget(File_location_Label, 4, 0)
        layout.addWidget(File_Size_Label, 5, 0)
        layout.addWidget(File_Created_Label, 6, 0)
        layout.addWidget(File_Modified_Label, 7, 0)
        layout.addWidget(public_key_label, 8, 0)
        layout.addWidget(public_Key_Entry, 8, 1)
        layout.addWidget(load_Public_Button, 10, 1)
        layout.addWidget(private_key_label, 11, 0)
        layout.addWidget(private_Key_Entry, 11, 1)
        layout.addWidget(save_Public_Button, 9, 1)
        layout.addWidget(load_private_Button, 12, 1)
        layout.addWidget(save_private_Button, 13, 1)
        layout.addWidget(enc, 14, 0)
        layout.addWidget(gen, 15, 0)
        layout.addWidget(Receiver_Browse_label, 1, 5)
        layout.addWidget(Recevier_Browse_Entry, 1, 6)
        layout.addWidget(Receiver_Browse_Button, 1, 7)
        layout.addWidget(public_Key_label,2, 5)
        layout.addWidget(Public_Key_Entry, 2, 6)
        layout.addWidget(Load_Button, 2, 7)
        layout.addWidget(Hash_Button, 3, 6)
        layout.addWidget(Decryption_Button, 4, 6)
        self.horizontalGroupBox.setLayout(layout)




app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
app = QApplication(sys.argv)
