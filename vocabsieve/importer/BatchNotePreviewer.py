from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from ..constants import LookUpResults
from .utils import *

class BatchNotePreviewer(QTextEdit):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.note_items = []
        self.setReadOnly(True)
        self.currentIndex = 0
        self.layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        buttons_box_widget = QWidget()
        self.layout.addWidget(buttons_box_widget)
        buttons_box_layout = QHBoxLayout(buttons_box_widget)

        first_button = QPushButton("<<")
        prev_button = QPushButton("<")
        self.counter = QLabel("0/0")
        self.counter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        next_button = QPushButton(">")
        last_button = QPushButton(">>")
        buttons_box_layout.addWidget(first_button)
        buttons_box_layout.addWidget(prev_button)
        buttons_box_layout.addWidget(self.counter)
        buttons_box_layout.addWidget(next_button)
        buttons_box_layout.addWidget(last_button)
        prev_button.clicked.connect(self.back)
        next_button.clicked.connect(self.forward)
        first_button.clicked.connect(self.first)
        last_button.clicked.connect(self.last)


    def appendNoteItem(self, sentence: str, item: LookUpResults, word_original: str):
        self.note_items.append((sentence, item, word_original))
        self.setCurrentIndex(len(self.note_items) - 1)
        
    def setCurrentIndex(self, index: int):
        self.currentIndex = index
        self.counter.setText(f"{index+1}/{len(self.note_items)}")
        self.setText(genPreviewHTML(*self.note_items[index]))
    
    def back(self):
        if self.currentIndex > 0:
            self.setCurrentIndex(self.currentIndex - 1)

    def forward(self):
        if self.currentIndex < len(self.note_items) - 1:
            self.setCurrentIndex(self.currentIndex + 1)

    def first(self):
        if self.note_items:
            self.setCurrentIndex(0)

    def last(self):
        if self.note_items:
            self.setCurrentIndex(len(self.note_items) - 1)

    def reset(self):
        self.note_items = []
        self.currentIndex = 0
        self.setText("")
        self.counter.setText("0/0")
