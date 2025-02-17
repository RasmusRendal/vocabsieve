from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from bidict import bidict
from ..dictionary import langs_supported, langcodes
import os
import pysubs2
from ..tools import *
from .utils import *

supported_content_formats = bidict({
    ".fb2": "Ebook (FictionBook)",
    ".epub": "Ebook (EPUB)",
    ".srt": "Subtitles (srt)",
    ".ass": "Subtitles (ass)",
    ".vtt": "Subtitles (vtt)",
    ".html": "HTML", 
    '.azw': "Ebook (azw)", 
    '.azw3': "Ebook (azw3)", 
    '.kfx': "Ebook (kfx)", 
    '.mobi': "Ebook (mobi)",
    "folder": "Folder"
})


class AddContentDialog(QDialog):
    def __init__(self, parent, path, folder=False):
        super().__init__(parent)
        self.settings = parent.settings
        self.parent = parent
        self.resize(400, 200)
        self.path = path
        self.setWindowTitle("Add content")

        if os.path.isdir(self.path):
            self.basename = os.path.basename(self.path)
            self.contenttype = "folder"
        else:
            basename, ext = os.path.splitext(self.path)
            self.basename = os.path.basename(basename)
            self.contenttype = ext
        if self.contenttype == None:
            raise NotImplementedError
        self.initWidgets()
        self.setupWidgets()

    def initWidgets(self):
        self.name = QLineEdit()
        self.name.setText(self.basename)
        self.lang = QComboBox()
        self.lang.addItems(langs_supported.values())
        self.lang.setCurrentText(
            langcodes[self.settings.value("target_language")])
        self.date = QDateEdit(QDate.currentDate())
        self.date.setDisplayFormat("yyyy-MM-dd")
        self.commit_button = QPushButton("Add")
        self.commit_button.clicked.connect(self.commit)

    def setupWidgets(self):
        self.layout = QFormLayout(self)
        self.layout.addRow(QLabel("Name"), self.name)
        self.layout.addRow(QLabel("Type"), QLabel(supported_content_formats[self.contenttype]))
        self.layout.addRow(QLabel("Language"), self.lang)
        self.layout.addRow(QLabel("Date"), self.date)
        self.layout.addRow(self.commit_button)

    def extractBook(self, path):
        return "\n".join(ebook2text(path)[0])

    def extractSubs(self, path):
        _, ext = os.path.splitext(path)
        subs = pysubs2.load(path, format_=ext[1:])
        return "\n".join(line.text for line in subs)
        


    def commit(self):
        if self.contenttype in ['.epub', '.fb2', '.azw', '.azw3', '.kfx', '.mobi' ]:
            content = self.extractBook(self.path)
        elif self.contenttype in ['.ass', '.srt', '.vtt']:
            content = self.extractSubs(self.path)
        elif self.contenttype == "folder":
            content = ""
            for file in os.listdir(self.path):
                try:
                    _, ext = os.path.splitext(file)
                    if ext in ['.epub', '.fb2', '.azw', '.azw3', '.kfx', '.mobi' ]:
                        content += self.extractBook(os.path.join(self.path, file)) + "\n\n"
                    elif ext in ['.ass', '.srt', '.vtt']:
                        content += self.extractSubs(os.path.join(self.path, file))
                except Exception as e:
                    print(repr(e))
                        
        self.parent.rec.importContent(
            self.name.text(),
            content,
            langcodes.inverse[self.lang.currentText()],
            self.date.date().toJulianDay()
            )
        self.parent.refresh()
        self.close()


    
