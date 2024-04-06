import os
import zipfile
import py7zr
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QMessageBox

class NESHeaderRemover(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Batch NES Header Remover')
        self.setGeometry(100, 100, 200, 100)
        
        self.layout = QVBoxLayout()
                
        self.btn = QPushButton('Choose Headered NES ROM Directory', self)
        self.btn.clicked.connect(self.chooseDirectory)
        self.layout.addWidget(self.btn)
        
        self.setLayout(self.layout)

    def chooseDirectory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Headered NES ROM Directory")
        if dir_path:
            self.extractArchives(dir_path)
            self.processNESFiles(dir_path)
            self.showCompletionMessage()

    def extractArchives(self, dir_path):
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            if filename.endswith('.zip'):
                self.extractZip(file_path, dir_path)
            elif filename.endswith('.7z'):
                self.extract7z(file_path, dir_path)

    def extractZip(self, archive_path, dir_path):
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(dir_path)
        os.remove(archive_path)

    def extract7z(self, archive_path, dir_path):
        with py7zr.SevenZipFile(archive_path, mode='r') as zip_ref:
            zip_ref.extractall(path=dir_path)
        os.remove(archive_path)

    def processNESFiles(self, dir_path):
        for filename in os.listdir(dir_path):
            if filename.endswith('.nes'):
                file_path = os.path.join(dir_path, filename)
                new_file_path = file_path[:-4] + '.unh'
                with open(file_path, 'rb') as file:
                    file.read(16)
                    file_content = file.read()
                
                with open(new_file_path, 'wb') as new_file:
                    new_file.write(file_content)
                
                os.remove(file_path)  # Comment out to retain the original file

    def showCompletionMessage(self):
        QMessageBox.information(self, "Processing Complete", "All files have been processed successfully.", QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication([])
    ex = NESHeaderRemover()
    ex.show()
    app.exec_()
