from itertools import tee
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QTextEdit, QGridLayout, QToolBar, QToolButton, QMenuBar, QLabel, QBoxLayout
from PyQt5.QtWidgets import QSlider, QStatusBar, QFileDialog, QInputDialog, QDialog, QRadioButton, QLineEdit, QMessageBox, QFontDialog, QColorDialog
from PyQt5.QtGui import QIcon, QFont, QCursor, QTextCursor, QColor, QCloseEvent
from PyQt5.QtCore import QSize, Qt

from sys import exit
from webbrowser import WindowsDefault
from datetime import datetime


root = R'media/'
background_gray = '#EAEAEA'
border_gray = '#A5A5A5'
number_of_app = 2


class Notepad (QWidget):
    def __init__(self):
        super().__init__()
        self.file_name = ''
        self.file_address = ''
        self.file_type = ''
        self.text_find = ''
        self.lst_find_index = []

        self.window()
        self.make_texts()
        self.make_file_menu()
        self.make_edit_menu()
        self.make_view_menu()
        self.make_about_menu()
        self.make_toolbar()
        self.make_status()

        self.main_textedit_font = self.text_edit.font().pointSize()

    def window(self):
        self.setGeometry(400, 200, 700, 550)
        self.setWindowTitle('ART Editor')
        self.setMinimumSize(300, 250)
        self.setStyleSheet('QWidget {background : #ECF3FA}')
        self.setWindowIcon(QIcon(root + 'notepad.png'))

        self.main_layout = QGridLayout(self)
        self.setLayout(self.main_layout)

        self.menubar = QMenuBar(self)
        self.menubar.setMaximumWidth(180)
        self.menubar.setStyleSheet(
            'QMenuBar {background-color : white; border : 2px solid #A5A5A5; border-radius : 5px}' +
            'QMenuBar::item:selected {background-color : lightblue}')
        self.main_layout.addWidget(self.menubar, 0, 0)

        self.clipboard = QApplication.clipboard()

    def make_texts(self):
        self.text_edit = QTextEdit(self)
        self.main_layout.addWidget(self.text_edit, 1, 0)
        self.text_edit.setFont(QFont('Arial', 12))
        self.text_edit.setStyleSheet(
            'background-color : white; border : 2px solid %s; border-radius : 5px;' % border_gray)

    def make_file_menu(self):
        self.file_menu = self.menubar.addMenu('File')
        self.file_menu.setStyleSheet(
            'QMenu {background-color : white; border :2px solid %s;}' % border_gray +
            'QMenu::item:selected {background-color : #91BCE3;}')
        self.file_menu.setCursor(QCursor(Qt.PointingHandCursor))

        # make action
        self.new = self.file_menu.addAction('New')
        self.open = self.file_menu.addAction('Open..')
        self.save = self.file_menu.addAction('Save')
        self.save_as = self.file_menu.addAction('Save as..')
        self.file_menu.addSeparator()
        self.exit = self.file_menu.addAction('Exit')

        # set icons
        self.new.setIcon(QIcon(root + 'new_file.png'))
        self.open.setIcon(QIcon(root + 'open_file.png'))
        self.save.setIcon(QIcon(root + 'save.png'))
        self.save_as.setIcon(QIcon(root + 'save_as.png'))
        self.exit.setIcon(QIcon(root + 'exit.png'))

        # set events
        self.new.triggered.connect(lambda: exec(
            f'window{number_of_app} = Notepad()\nwindow{number_of_app}.show()\nnumber_of_app += 1'))
        self.open.triggered.connect(lambda: Events.open_file(self))
        self.save.triggered.connect(lambda: Events.save_file(self))
        self.save_as.triggered.connect(lambda: Events.save_as_file(self))
        self.exit.triggered.connect(lambda: self.close())

    def make_edit_menu(self):
        self.edit_menu = self.menubar.addMenu('Edit')
        self.edit_menu.setStyleSheet(
            'QMenu {background-color : white; border :2px solid %s;}' % border_gray + 'QMenu::item:selected {background-color : #91BCE3;}')
        self.edit_menu.setCursor(QCursor(Qt.PointingHandCursor))

        # make actions
        self.undo = self.edit_menu.addAction('Undo')
        self.redo = self.edit_menu.addAction('Redo')
        self.edit_menu.addSeparator()
        self.cut = self.edit_menu.addAction('Cut')
        self.copy = self.edit_menu.addAction('Copy')
        self.paste = self.edit_menu.addAction('Paste')
        self.delete = self.edit_menu.addAction('Delete')
        self.clear = self.edit_menu.addAction('Clear')
        self.edit_menu.addSeparator()
        self.find_text = self.edit_menu.addAction('Find')
        self.find_next = self.edit_menu.addAction('Find Next')
        self.goto = self.edit_menu.addAction('Go to ..')
        self.replace = self.edit_menu.addAction('Replace')
        self.search_google = self.edit_menu.addAction('Search In Google')
        self.select_all = self.edit_menu.addAction('Select All')
        self.edit_menu.addSeparator()
        self.date_time = self.edit_menu.addAction('Date & Time')
        self.change_font = self.edit_menu.addAction('Font')
        self.change_color = self.edit_menu.addAction('foreground Color')
        self.change_background = self.edit_menu.addAction(
            'Background Color')
        self.change_highlight = self.edit_menu.addAction(
            'Highlight Color')
        self.change_alignment = self.edit_menu.addAction('Alignment')

        # set icons
        self.undo.setIcon(QIcon(root + 'undo.png'))
        self.redo.setIcon(QIcon(root + 'redo.png'))
        self.copy.setIcon(QIcon(root + 'copy.png'))
        self.cut.setIcon(QIcon(root + 'cut.png'))
        self.paste.setIcon(QIcon(root + 'paste.png'))
        self.delete.setIcon(QIcon(root + 'delete.png'))
        self.clear.setIcon(QIcon(root + 'clear.png'))
        self.find_text.setIcon(QIcon(root + 'find.png'))
        self.find_next.setIcon(QIcon(root + 'find_next.png'))
        self.goto.setIcon(QIcon(root + 'go_to.png'))
        self.replace.setIcon(QIcon(root + 'replace.png'))
        self.search_google.setIcon(QIcon(root + 'search_google.png'))
        self.select_all.setIcon(QIcon(root + 'selection.png'))
        self.date_time.setIcon(QIcon(root + 'date_time.png'))
        self.change_font.setIcon(QIcon(root + 'font.png'))
        self.change_color.setIcon(QIcon(root + 'font_color.png'))
        self.change_background.setIcon(QIcon(root + 'background_color.png'))
        self.change_highlight.setIcon(QIcon(root + 'highlight_color.png'))
        self.change_alignment.setIcon(QIcon(root + 'alignment.png'))

        # set events
        self.undo.triggered.connect(lambda: self.text_edit.undo())
        self.redo.triggered.connect(lambda: self.text_edit.redo())
        self.copy.triggered.connect(lambda: self.text_edit.copy())
        self.cut.triggered.connect(lambda: self.text_edit.cut())
        self.paste.triggered.connect(lambda: self.text_edit.paste())
        self.delete.triggered.connect(
            lambda: self.text_edit.textCursor().deletePreviousChar())
        self.clear.triggered.connect(
            lambda: self.text_edit.setText(''))
        self.find_text.triggered.connect(lambda: Events.find_text(self))
        self.find_next.triggered.connect(lambda: Events.find_next(self))
        self.goto.triggered.connect(lambda: Events.go_to(self))
        self.replace.triggered.connect(lambda: Events.replace(self))
        self.search_google.triggered.connect(
            lambda: Events.search_google(self))
        self.select_all.triggered.connect(lambda: self.text_edit.selectAll())
        self.date_time.triggered.connect(lambda: Events.date_time(self))
        self.change_font.triggered.connect(lambda: Events.change_font(self))
        self.change_color.triggered.connect(lambda: Events.change_color(self))
        self.change_background.triggered.connect(
            lambda: Events.change_background(self))
        self.change_highlight.triggered.connect(
            lambda: Events.highlight_color(self))
        self.change_alignment.triggered.connect(
            lambda: Events.change_alignment(self))

    def make_view_menu(self):
        self.view_menu = self.menubar.addMenu('View')
        self.view_menu.setStyleSheet(
            'QMenu {background-color : white; border :2px solid %s;}' % border_gray + 'QMenu::item:selected {background-color : #91BCE3;}')
        self.view_menu.setCursor(QCursor(Qt.PointingHandCursor))

        self.change_zoom = 0

        # make actions
        self.zoom_in = self.view_menu.addAction('Zoom in')
        self.zoom_out = self.view_menu.addAction('Zoom out')
        self.zoom_100 = self.view_menu.addAction('Zoom 100%')

        # set icons
        self.zoom_in.setIcon(QIcon(root + 'zoom_in.png'))
        self.zoom_out.setIcon(QIcon(root + 'zoom_out.png'))
        self.zoom_100.setIcon(QIcon(root + 'zoom_100.png'))

        # set events
        self.zoom_in.triggered.connect(lambda: Events.zoom_in(self))
        self.zoom_out.triggered.connect(lambda: Events.zoom_out(self))
        self.zoom_100.triggered.connect(lambda: Events.zoom_100(self))

    def make_about_menu(self):
        self.about_menu = self.menubar.addMenu('About')
        self.about_menu.setStyleSheet(
            'QMenu {background-color : white; border :2px solid %s;}' % border_gray + 'QMenu::item:selected {background-color : #91BCE3;}')
        self.about_menu.setCursor(QCursor(Qt.PointingHandCursor))

        def on_click():
            dialog = QDialog(self)
            dialog.setGeometry(600, 300, 300, 220)
            dialog.setFixedSize(300, 220)
            dialog.setWindowTitle('About us')

            lb = QLabel(dialog)
            lb.setStyleSheet('color : darkblue;')
            lb.setGeometry(10, 10, 280, 200)
            lb.setWordWrap(True)
            lb.setText(
                """This software (ART Editor) is a Text Editor with many options and was made by "AmirReza Tavallaei" and is available for free.\nemail : tavallaei.14@gmail.com\nPhone: 09132692407\n\nAny copying is illegal.\ngood luck ...""")
            lb.setAlignment(Qt.AlignLeft)
            lb.setFont(QFont('Tahoma', 13))

            btn = QPushButton(dialog)
            btn.setStyleSheet('background-color : #ECF3FA; border: 0px')
            btn.setGeometry(220, 140, 45, 45)
            btn.setIcon(QIcon(root + 'notepad.png'))
            btn.setIconSize(QSize(45, 45))

            dialog.show()

        self.about = self.about_menu.addAction('About us')
        self.about.setIcon(QIcon(root + 'information.png'))
        self.about.triggered.connect(lambda: on_click())

    def make_toolbar(self):
        self.btn_show_toolbar = QPushButton()
        self.main_layout.addWidget(self.btn_show_toolbar, 0, 1)
        self.btn_show_toolbar.setIcon(QIcon(root + 'toolbar.png'))
        self.btn_show_toolbar.setStyleSheet(
            'QPushButton {background-color : white; border : 2px solid %s;}' % border_gray +
            'QPushButton::Hover {background-color : %s;}' % background_gray)
        self.btn_show_toolbar.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_show_toolbar.setIconSize(QSize(35, 20))
        self.btn_show_toolbar.clicked.connect(self.show_toolbar)
        self.btn_show_toolbar.setToolTip('Show/Hide ToolBar')

        self.btn_show_toolbar.setMinimumHeight(25)
        self.btn_show_toolbar.setMinimumWidth(35)
        self.btn_show_toolbar.setMaximumHeight(25)
        self.btn_show_toolbar.setMaximumWidth(35)

        ######################################################################

        self.toolbar = QToolBar(self)
        self.toolbar.setOrientation(Qt.Vertical)
        self.main_layout.addWidget(self.toolbar, 1, 1)
        self.toolbar.setStyleSheet(
            'QToolBar {background-color : %s; border : 2px solid %s; border-radius : 5px;}' % (background_gray, border_gray))
        self.toolbar.setMaximumHeight(390)
        self.toolbar.setMinimumWidth(40)
        self.toolbar.setToolTip('ToolBar')

        ######################################################################

        self.new_toolbar = QToolButton()
        self.new_toolbar.setStyleSheet(
            'background-color : %s' % background_gray)
        self.new_toolbar.setCursor(QCursor(Qt.PointingHandCursor))
        self.new_toolbar.setIcon(QIcon(root + 'new_file.png'))
        self.toolbar.addWidget(self.new_toolbar)
        self.new_toolbar.clicked.connect(lambda: exec(
            f'window{number_of_app} = Notepad()\nwindow{number_of_app}.show()\nnumber_of_app += 1'))
        self.new_toolbar.setToolTip('New File')

        self.toolbar.addSeparator()

        self.open_toolbar = QToolButton()
        self.open_toolbar.setStyleSheet(
            'background-color : %s' % background_gray)
        self.open_toolbar.setCursor(QCursor(Qt.PointingHandCursor))
        self.open_toolbar.setIcon(QIcon(root + 'open_file.png'))
        self.toolbar.addWidget(self.open_toolbar)
        self.open_toolbar.clicked.connect(lambda: Events.open_file(self))
        self.open_toolbar.setToolTip('Open a File')

        self.toolbar.addSeparator()

        self.save_toolbar = QToolButton()
        self.save_toolbar.setStyleSheet(
            'background-color : %s' % background_gray)
        self.save_toolbar.setCursor(QCursor(Qt.PointingHandCursor))
        self.save_toolbar.setIcon(QIcon(root + 'save.png'))
        self.toolbar.addWidget(self.save_toolbar)
        self.save_toolbar.clicked.connect(lambda: Events.save_file(self))
        self.save_toolbar.setToolTip('Save File')

        self.toolbar.addSeparator()

        self.save_as_toolbar = QToolButton()
        self.save_as_toolbar.setStyleSheet(
            'background-color : %s' % background_gray)
        self.save_as_toolbar.setCursor(QCursor(Qt.PointingHandCursor))
        self.save_as_toolbar.setIcon(QIcon(root + 'save_as.png'))
        self.toolbar.addWidget(self.save_as_toolbar)
        self.save_as_toolbar.clicked.connect(
            lambda: Events.save_as_file(self))
        self.save_as_toolbar.setToolTip('Save as File')

        self.toolbar.addSeparator()

        self.undo_toolbar = QToolButton()
        self.undo_toolbar.setStyleSheet(
            'background-color : %s' % background_gray)
        self.undo_toolbar.setCursor(QCursor(Qt.PointingHandCursor))
        self.undo_toolbar.setIcon(QIcon(root + 'undo.png'))
        self.toolbar.addWidget(self.undo_toolbar)
        self.undo_toolbar.clicked.connect(lambda: self.text_edit.undo())
        self.undo_toolbar.setToolTip('Undo')

        self.toolbar.addSeparator()

        self.redo_toolbar = QToolButton()
        self.redo_toolbar.setStyleSheet(
            'background-color : %s' % background_gray)
        self.redo_toolbar.setCursor(QCursor(Qt.PointingHandCursor))
        self.redo_toolbar.setIcon(QIcon(root + 'redo.png'))
        self.toolbar.addWidget(self.redo_toolbar)
        self.redo_toolbar.clicked.connect(lambda: self.text_edit.redo())
        self.redo_toolbar.setToolTip('Redo')

        self.toolbar.addSeparator()

        self.font_toolbar = QToolButton()
        self.font_toolbar.setStyleSheet(
            'background-color : %s' % background_gray)
        self.font_toolbar.setCursor(QCursor(Qt.PointingHandCursor))
        self.font_toolbar.setIcon(QIcon(root + 'font.png'))
        self.toolbar.addWidget(self.font_toolbar)
        self.font_toolbar.clicked.connect(lambda: Events.change_font(self))
        self.font_toolbar.setToolTip('Change Font')

        self.toolbar.addSeparator()

        self.color_toolbar = QToolButton()
        self.color_toolbar.setStyleSheet(
            'background-color : %s' % background_gray)
        self.color_toolbar.setCursor(QCursor(Qt.PointingHandCursor))
        self.color_toolbar.setIcon(QIcon(root + 'font_color.png'))
        self.toolbar.addWidget(self.color_toolbar)
        self.color_toolbar.clicked.connect(lambda: Events.change_color(self))
        self.color_toolbar.setToolTip('Change Text Color')

        self.toolbar.addSeparator()

        self.background_color_toolbar = QToolButton()
        self.background_color_toolbar.setStyleSheet(
            'background-color : %s' % background_gray)
        self.background_color_toolbar.setCursor(QCursor(Qt.PointingHandCursor))
        self.background_color_toolbar.setIcon(
            QIcon(root + 'background_color.png'))
        self.toolbar.addWidget(self.background_color_toolbar)
        self.background_color_toolbar.clicked.connect(
            lambda: Events.change_background(self))
        self.background_color_toolbar.setToolTip('Change Background Color')

        self.toolbar.addSeparator()

        self.highlight_color_toolbar = QToolButton()
        self.highlight_color_toolbar.setStyleSheet(
            'background-color : %s' % background_gray)
        self.highlight_color_toolbar.setCursor(QCursor(Qt.PointingHandCursor))
        self.highlight_color_toolbar.setIcon(
            QIcon(root + 'highlight_color.png'))
        self.toolbar.addWidget(self.highlight_color_toolbar)
        self.highlight_color_toolbar.clicked.connect(
            lambda: Events.highlight_color(self))
        self.highlight_color_toolbar.setToolTip('Change highlight Color')

    def make_status(self):
        self.status = QStatusBar(self)
        self.main_layout.addWidget(self.status, 2, 0, 1, 3)
        self.status.setStyleSheet(
            'QStatusBar {background-color : %s; border: 2px solid %s; border-radius : 5px;}' % (background_gray, border_gray))
        self.status.setSizeGripEnabled(False)
        self.status.setToolTip('Status bar')

        style = 'background-color : %s;' % background_gray

        ##############################################################################

        self.lb_name_project = QLabel(self.status)
        self.lb_name_project.setText('Untitled.txt')
        self.lb_name_project.setAlignment(Qt.AlignCenter)
        self.lb_name_project.setStyleSheet(style)
        self.lb_name_project.setToolTip('File Name')

        self.lb_row_column_text = QLabel(self.status)
        self.lb_row_column_text.setText(
            f'Row {self.text_edit.textCursor().columnNumber()} | Character {self.text_edit.textCursor().columnNumber()}')
        self.lb_row_column_text.setAlignment(Qt.AlignCenter)
        self.lb_row_column_text.setStyleSheet(style)
        self.lb_row_column_text.setMinimumWidth(150)
        self.lb_row_column_text.setToolTip('Current Row & Character')

        ##############################################

        self.text_edit.textChanged.connect(lambda: self.lb_row_column_text.setText(
            f'Row {self.text_edit.textCursor().blockNumber()+1} | Character {self.text_edit.textCursor().columnNumber()}'))

        self.text_edit.selectionChanged.connect(lambda: self.lb_row_column_text.setText(
            f'Row {self.text_edit.textCursor().blockNumber()+1} | Character {self.text_edit.textCursor().columnNumber()}'))

        ##############################################

        self.zoom_slider = QSlider(self.status)
        self.zoom_slider.setRange(1, 200)
        self.zoom_slider.setValue(100)
        self.zoom_slider.setOrientation(Qt.Horizontal)
        self.zoom_slider.setStyleSheet(style)
        self.zoom_slider.setMaximumHeight(20)
        self.zoom_slider.setSingleStep(10)
        self.zoom_slider.setPageStep(10)
        self.zoom_slider.setTickInterval(10)
        self.zoom_slider.setTickPosition(QSlider.TicksBelow)
        self.zoom_slider.sliderMoved.connect(
            lambda: Events.set_zoom_slider(self))

        self.btn_plus_zoom = QToolButton(self.status)
        self.btn_plus_zoom.setAutoRaise(True)
        self.btn_plus_zoom.setText('+')
        self.btn_plus_zoom.setMaximumWidth(20)
        self.btn_plus_zoom.setMinimumWidth(20)
        self.btn_plus_zoom.setStyleSheet(
            style + 'color: darkblue;')
        self.btn_plus_zoom.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_plus_zoom.setFont(QFont('Arial', 10))
        self.btn_plus_zoom.clicked.connect(lambda: Events.zoom_in(self))
        self.btn_plus_zoom.setToolTip('Plus 5 Zoom')

        self.btn_minus_zoom = QToolButton(self.status)
        self.btn_minus_zoom.setAutoRaise(True)
        self.btn_minus_zoom.setText('-')
        self.btn_minus_zoom.setMaximumWidth(20)
        self.btn_minus_zoom.setMinimumWidth(20)
        self.btn_minus_zoom.setStyleSheet(
            style + 'color: darkblue;')
        self.btn_minus_zoom.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_minus_zoom.setFont(QFont('Arial', 13))
        self.btn_minus_zoom.clicked.connect(lambda: Events.zoom_out(self))
        self.btn_minus_zoom.setToolTip('minus 5 Zoom')

        self.zoom = QLabel(self.status)
        self.zoom.setText(str(self.zoom_slider.value()) + '%')
        self.zoom.setMinimumWidth(30)
        self.zoom.setStyleSheet(style)
        self.zoom.setToolTip('Zoom')

        self.lb_space = QLabel()
        self.lb_space.setMinimumWidth(10)
        self.lb_space.setStyleSheet(
            style + 'border-right: 2px solid %s' % border_gray)

        ##############################################################################

        self.status.addWidget(self.lb_name_project, 1)
        self.status.addWidget(self.lb_row_column_text, 1)
        self.status.addWidget(self.zoom)
        self.status.addWidget(self.btn_minus_zoom, 1)
        self.status.addWidget(self.zoom_slider, 1)
        self.status.addWidget(self.btn_plus_zoom, 1)
        self.status.addWidget(self.lb_space)

    def show_toolbar(self):
        if self.toolbar.isHidden():
            self.main_layout.addWidget(self.toolbar, 1, 1)
            self.toolbar.show()
            self.main_layout.addWidget(self.text_edit, 1, 0, 1, 1)
            self.main_layout.addWidget(self.btn_show_toolbar, 0, 1)
            self.btn_show_toolbar.setIcon(QIcon(root + 'toolbar.png'))
        else:
            self.toolbar.hide()
            self.main_layout.addWidget(self.text_edit, 1, 0, 1, 3)
            self.main_layout.addWidget(self.btn_show_toolbar, 0, 2)
            self.btn_show_toolbar.setIcon(QIcon(root + 'toolbar2.png'))


class Events(Notepad):
    def __init__(self):
        Notepad.__init__()

    def open_file(self):
        dialog = QFileDialog(self)
        file_address = dialog.getOpenFileName(
            self, 'Choose a file', '', 'Text Files (*.txt);; All Files (*.*)')[0]

        if file_address != '':
            with open(file_address, 'r') as file:
                text = file.read()
                exec(
                    f'window{number_of_app} = Notepad()\nwindow{number_of_app}.show()\nwindow{number_of_app}.text_edit.setText(text)\n' +
                    f'window{number_of_app}.file_name = file_address.split("/")[-1]\nwindow{number_of_app}.file_address = file_address\n' +
                    f'window{number_of_app}.file_type = window.file_name.split(".")[-1]\n' +
                    f'window{number_of_app}.lb_name_project.setText(window{number_of_app}.file_name)\nnumber_of_app += 1')

    def save_file(self):
        if self.file_name != '' and self.file_address != '':
            with open(self.file_address, 'w') as file:
                file.write(self.text_edit.toPlainText())
        else:
            Events.save_as_file(self)

    def save_as_file(self):
        dialog = QFileDialog(self)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_address = dialog.getSaveFileName(
            self, 'Save file as', '', 'Text Files (*.txt);; All Files(*.*)')[0]

        if file_address != '':
            with open(file_address, 'w') as file:
                file.write(self.text_edit.toPlainText())
                self.file_name = file_address.split('/')[-1]
                self.file_address = file_address
                self.file_type = self.file_name.split('.')[-1]
                self.lb_name_project.setText(self.file_name)

    def zoom_in(self):
        if self.zoom_slider.value() <= 200:
            if self.zoom_slider.value() < 100:
                if self.zoom_slider.value() > 100 - self.main_textedit_font:
                    self.text_edit.zoomIn(5)
            else:
                self.text_edit.zoomIn(5)
            self.change_zoom += 5
            self.zoom_slider.setValue(self.zoom_slider.value() + 5)
            self.zoom.setText(str(self.zoom_slider.value()) + '%')

    def zoom_out(self):
        if self.zoom_slider.value() >= 1:
            if self.text_edit.font().pointSize() > 1:
                self.text_edit.zoomOut(5)
            self.change_zoom -= 5
            self.zoom_slider.setValue(self.zoom_slider.value() - 5)

        self.zoom.setText(str(self.zoom_slider.value()) + '%')

    def zoom_100(self):
        font = self.text_edit.font()
        font.setPointSize(self.main_textedit_font)
        self.text_edit.setFont(font)
        self.change_zoom = 0
        self.zoom_slider.setValue(100)
        self.zoom.setText(str(self.zoom_slider.value()) + '%')

    def set_zoom_slider(self):
        if self.zoom_slider.value() - 100 > self.change_zoom:
            zoom = self.zoom_slider.value() - 100 - self.change_zoom
            self.change_zoom += zoom

            if self.zoom_slider.value() < 100:
                if self.zoom_slider.value() > 100 - self.main_textedit_font:
                    self.text_edit.zoomIn(zoom)
            else:
                self.text_edit.zoomIn(zoom)
        else:
            zoom = self.change_zoom - (self.zoom_slider.value() - 100)
            self.text_edit.zoomOut(zoom)
            self.change_zoom -= zoom

        self.zoom.setText(str(self.zoom_slider.value()) + '%')

    def find_text(self):
        dialog = QInputDialog(self)
        dialog.setOkButtonText('Find')
        dialog.setStyleSheet(
            'QInputDialog {background-color : #F5F9FD;} QInputDialog QPushButton {background-color : %s; border-radius : 5px; color: white; font-family: Arial; font-size : 10pt; width : 55px; height : 20px}' % border_gray)

        self.text_find, ok = dialog.getText(
            dialog, 'Find..', 'Enter a value for find in file: ', text=self.text_find)

        if ok:
            self.text_edit.moveCursor(1)
            self.text_edit.find(self.text_find)
            self.lst_find_index.append(
                self.text_edit.toPlainText().find(self.text_find))

    def find_next(self):
        if self.text_find != '':
            text = self.text_edit.toPlainText()
            index = None
            plus_index = 0
            while index == None or index in self.lst_find_index:
                if self.text_find in text:
                    index = text.find(self.text_find) + plus_index
                    text = text[:text.find(self.text_find)] + \
                        text[text.find(self.text_find)+len(self.text_find):]
                    plus_index += len(self.text_find)
                else:
                    break

            self.lst_find_index.append(index)

            cursor = self.text_edit.textCursor()
            cursor.setPosition(index)
            cursor.setPosition(index+len(self.text_find),
                               QTextCursor.KeepAnchor)
            self.text_edit.setTextCursor(cursor)

    def go_to(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Go to ..')
        dialog.setFixedSize(230, 125)
        dialog.setStyleSheet(
            'background-color : #F5F9FD;')
        dialog.show()

        layout = QGridLayout(dialog)
        dialog.setLayout(layout)

        lb = QLabel('Select a mode and enter a number: ', dialog)
        lb.setStyleSheet('font-family: Arial; font-size: 10pt')
        layout.addWidget(lb, 0, 0, 1, 2)

        rd_btn1 = QRadioButton('Go To Line: ', dialog)
        rd_btn1.setStyleSheet('font-family: Arial; font-size: 10pt')
        le_1 = QLineEdit(dialog)
        layout.addWidget(rd_btn1, 1, 0, 1, 1)
        layout.addWidget(le_1, 1, 1, 1, 1)

        rd_btn2 = QRadioButton('Go To Word: ', dialog)
        rd_btn2.setStyleSheet('font-family: Arial; font-size: 10pt')
        le_2 = QLineEdit(dialog)
        layout.addWidget(rd_btn2, 2, 0, 1, 1)
        layout.addWidget(le_2, 2, 1, 1, 1)

        def enable_btn1():
            le_2.setEnabled(False)
            le_1.setEnabled(True)

        def enable_btn2():
            le_2.setEnabled(True)
            le_1.setEnabled(False)

        rd_btn1.clicked.connect(enable_btn1)
        rd_btn2.clicked.connect(enable_btn2)
        rd_btn1.setChecked(True)
        le_2.setEnabled(False)

        def go():
            if rd_btn1.isChecked():
                if le_1.text().isdigit():

                    text = self.text_edit.toPlainText()
                    text = text.split('\n')

                    if int(le_1.text()) not in range(1, len(text)+1):
                        msg = QMessageBox(self)
                        msg.setStyleSheet('background-color : #F5F9FD')
                        msg.setWindowTitle('Go To Line Error')
                        msg.setText(
                            'Line number is not in the range of line numbers')
                        msg.setStandardButtons(QMessageBox.Ok)
                        msg.show()
                    else:
                        if le_1.text() == '1':
                            index = 0
                        else:
                            index = len('\n'.join(text[:int(le_1.text())-1]))+1

                        cursor = self.text_edit.textCursor()
                        cursor.setPosition(index)
                        self.text_edit.setTextCursor(cursor)
                        dialog.close()
                else:
                    msg = QMessageBox(self)
                    msg.setStyleSheet('background-color : #F5F9FD')
                    msg.setWindowTitle('Go To Line Error')
                    msg.setText(
                        'Line number is invalid')
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.show()
            else:
                if le_2.text().isdigit():
                    text = self.text_edit.toPlainText()
                    text = text.split(' ')

                    if int(le_2.text()) not in range(1, len(text)+1):
                        msg = QMessageBox(self)
                        msg.setStyleSheet('background-color : #F5F9FD')
                        msg.setWindowTitle('Go To Line Error')
                        msg.setText(
                            'Word number is not in the range of number of words')
                        msg.setStandardButtons(QMessageBox.Ok)
                        msg.show()
                    else:
                        word = text[int(le_2.text())-1]
                        self.text_edit.moveCursor(1)
                        self.text_edit.find(word)
                        dialog.close()

                else:
                    msg = QMessageBox(self)
                    msg.setStyleSheet('background-color : #F5F9FD')
                    msg.setWindowTitle('Go To Line Error')
                    msg.setText(
                        'Word number is invalid')
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.show()

        btn_go = QPushButton('Go', dialog)
        btn_go.setMinimumHeight(20)
        btn_go.setStyleSheet(
            'background-color : %s; border-radius : 5px; color: white; font-family: Arial; font-size : 10pt' % border_gray)
        btn_go.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(btn_go, 3, 0, 1, 1)
        btn_go.clicked.connect(go)

        btn_cancel = QPushButton('Cancel', dialog)
        btn_cancel.setMinimumHeight(20)
        btn_cancel.setStyleSheet(
            'background-color : %s; border-radius : 5px; color: white; font-family: Arial; font-size : 10pt' % border_gray)
        btn_cancel.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(btn_cancel, 3, 1, 1, 1)
        btn_cancel.clicked.connect(lambda: dialog.close())

    def replace(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Replace..')
        dialog.setFixedSize(270, 120)
        dialog.setStyleSheet(
            'background-color : #F5F9FD;')
        dialog.show()

        layout = QGridLayout(dialog)
        dialog.setLayout(layout)

        lb1 = QLabel('Word 1: ', dialog)
        lb1.setStyleSheet('font-family: Arial; font-size: 10pt')
        layout.addWidget(lb1, 0, 0)
        le_1 = QLineEdit(dialog)
        le_1.setMinimumWidth(150)
        layout.addWidget(le_1, 0, 1)

        lb2 = QLabel('Word 2: ', dialog)
        lb2.setStyleSheet('font-family: Arial; font-size: 10pt')
        layout.addWidget(lb2, 1, 0)
        le_2 = QLineEdit(dialog)
        le_2.setMinimumWidth(150)
        layout.addWidget(le_2, 1, 1)

        #############################################

        def replace_one():
            text1 = le_1.text()
            text2 = le_2.text()

            all_text = self.text_edit.toPlainText()
            all_text = all_text.replace(text1, text2, 1)
            self.text_edit.setText(all_text)

        def replace_all():
            text1 = le_1.text()
            text2 = le_2.text()

            all_text = self.text_edit.toPlainText()
            all_text = all_text.replace(text1, text2)
            self.text_edit.setText(all_text)

        #############################################

        btn_replace = QPushButton('Replace One', dialog)
        btn_replace.setMinimumSize(85, 25)
        btn_replace.setStyleSheet(
            'background-color : %s; border-radius : 5px; color: white; font-family: Arial; font-size : 10pt' % border_gray)
        btn_replace.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(btn_replace, 2, 0)
        btn_replace.clicked.connect(replace_one)

        btn_replace_all = QPushButton('Replace All', dialog)
        btn_replace_all.setFixedSize(80, 25)
        btn_replace_all.setStyleSheet(
            'background-color : %s; border-radius : 5px; color: white; font-family: Arial; font-size : 10pt' % border_gray)
        btn_replace_all.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(btn_replace_all, 2, 1)
        btn_replace_all.clicked.connect(replace_all)

        btn_cancel = QPushButton('Cancel', dialog)
        btn_cancel.setMinimumSize(70, 25)
        btn_cancel.setStyleSheet(
            'background-color : %s; border-radius : 5px; color: white; font-family: Arial; font-size : 10pt' % border_gray)
        btn_cancel.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(btn_cancel, 2, 2)
        btn_cancel.clicked.connect(lambda: dialog.close())

    def search_google(self):
        word = self.text_edit.textCursor().selectedText()
        url = "https://www.google.com.tr/search?q={}".format(word)
        browser = WindowsDefault()
        browser.open_new_tab(url)

    def date_time(self):
        now = datetime.today().strftime('%d/%m/%Y  %H:%M')
        self.text_edit.insertPlainText(now)

    def change_font(self):
        dialog = QFontDialog(self)
        font, ok = dialog.getFont(
            QFont(self.text_edit.font()), self, 'Select a font')

        if ok:
            self.text_edit.setFont(font)
            self.main_textedit_font = font.pointSize()
            self.zoom_slider.setValue(100)
            self.zoom.setText('100%')
            self.change_zoom = 0

    def change_color(self):
        dialog = QColorDialog(self)
        color = dialog.getColor(
            self.text_edit.textColor(), self, 'Select a text color')

        self.text_edit.setTextColor(color)

    def change_background(self):
        dialog = QColorDialog(self)
        color = dialog.getColor(
            QColor('white'), self, 'Select a text color')

        self.text_edit.setStyleSheet(
            'background-color : %s; border : 2px solid %s; border-radius : 5px;' % (color.name(), border_gray))

    def highlight_color(self):
        dialog = QColorDialog(self)
        color = dialog.getColor(
            self.text_edit.textBackgroundColor(), self, 'Select a text color')

        self.text_edit.setTextBackgroundColor(color)

    def change_alignment(self):
        dialog = QDialog(self)
        dialog.setStyleSheet('background-color : #F5F9FD')
        dialog.setWindowTitle('Change Alignment')
        dialog.setFixedSize(200, 200)
        dialog.show()

        layout = QGridLayout(dialog)
        layout.setVerticalSpacing(15)
        dialog.setLayout(layout)

        lb = QLabel('Select an Alignment: ', dialog)
        lb.setFont(QFont('Titr', 12))
        layout.addWidget(lb, 0, 0, 1, 4)

        ###########################################################

        hbox1 = QBoxLayout(QBoxLayout.LeftToRight)
        layout.addLayout(hbox1, 1, 0, 1, 4)

        def select_btn():
            selected_btn = self.sender()
            selected_btn.setStyleSheet('background-color: #B7ECFF')
            if selected_btn.isChecked():
                for btn in [btn1, btn2, btn3]:
                    if btn != selected_btn and btn.isChecked():
                        btn.setChecked(False)
                        btn.setStyleSheet('background-color : #F5F9FD')
            else:
                for btn in [btn1, btn2, btn3]:
                    if btn.isChecked():
                        break
                selected_btn.setChecked(True)

        btn1 = QToolButton(self)
        btn1.setFixedSize(35, 35)
        btn1.setIconSize(QSize(25, 25))
        btn1.setCheckable(True)
        btn1.setIcon(QIcon(root + 'align_left'))
        btn1.clicked.connect(select_btn)
        hbox1.addWidget(btn1)

        btn2 = QToolButton(self)
        btn2.setFixedSize(35, 35)
        btn2.setIconSize(QSize(25, 25))
        btn2.setCheckable(True)
        btn2.setIcon(QIcon(root + 'align_center'))
        btn2.clicked.connect(select_btn)
        hbox1.addWidget(btn2)

        btn3 = QToolButton(self)
        btn3.setFixedSize(35, 35)
        btn3.setIconSize(QSize(25, 25))
        btn3.setCheckable(True)
        btn3.setIcon(QIcon(root + 'align_right'))
        btn3.clicked.connect(select_btn)
        hbox1.addWidget(btn3)

        ###########################################################

        hbox2 = QBoxLayout(QBoxLayout.LeftToRight)
        layout.addLayout(hbox2, 2, 0, 1, 4)

        def select_btn2():
            selected_btn = self.sender()
            selected_btn.setStyleSheet('background-color: #B7ECFF')
            if selected_btn.isChecked():
                for btn in [btn4, btn5]:
                    if btn != selected_btn and btn.isChecked():
                        btn.setChecked(False)
                        btn.setStyleSheet('background-color : #F5F9FD')
            else:
                for btn in [btn4, btn5]:
                    if btn.isChecked():
                        break
                selected_btn.setChecked(True)

        btn4 = QToolButton(self)
        btn4.setFixedSize(35, 35)
        btn4.setIconSize(QSize(25, 25))
        btn4.setCheckable(True)
        btn4.setIcon(QIcon(root + 'left_to_right_direction'))
        btn4.clicked.connect(select_btn2)
        hbox2.addWidget(btn4)

        btn5 = QToolButton(self)
        btn5.setFixedSize(35, 35)
        btn5.setIconSize(QSize(25, 25))
        btn5.setCheckable(True)
        btn5.setIcon(QIcon(root + 'right_to_left_direction'))
        btn5.clicked.connect(select_btn2)
        hbox2.addWidget(btn5)

        ###########################################################

        hbox3 = QBoxLayout(QBoxLayout.LeftToRight)
        layout.addLayout(hbox3, 3, 0, 1, 4)

        def on_click():
            if btn1.isChecked():
                self.text_edit.setAlignment(Qt.AlignLeft)
            elif btn2.isChecked():
                self.text_edit.setAlignment(Qt.AlignCenter)
            else:
                self.text_edit.setAlignment(Qt.AlignRight)

            if btn4.isChecked():
                self.text_edit.setLayoutDirection(Qt.LeftToRight)
            else:
                self.text_edit.setLayoutDirection(Qt.RightToLeft)

            dialog.close()

        btn6 = QPushButton('Ok', self)
        btn6.setCursor(Qt.PointingHandCursor)
        btn6.setFixedSize(70, 20)
        btn6.setStyleSheet(
            'background-color : %s; border-radius : 5px; color: white; font-family: Arial; font-size : 10pt' % border_gray)
        btn6.clicked.connect(on_click)
        hbox3.addWidget(btn6)

        btn7 = QPushButton('Cancel', self)
        btn7.setCursor(Qt.PointingHandCursor)
        btn7.setFixedSize(70, 20)
        btn7.setStyleSheet(
            'background-color : %s; border-radius : 5px; color: white; font-family: Arial; font-size : 10pt' % border_gray)
        btn7.clicked.connect(lambda: dialog.close())
        hbox3.addWidget(btn7)

        if self.text_edit.layoutDirection() == Qt.RightToLeft:
            btn5.setChecked(True)
            btn5.setStyleSheet('background-color: #B7ECFF')
        else:
            btn4.setChecked(True)
            btn4.setStyleSheet('background-color: #B7ECFF')

        if self.text_edit.alignment() == Qt.AlignRight:
            btn3.setChecked(True)
            btn3.setStyleSheet('background-color: #B7ECFF')
        elif self.text_edit.alignment() == Qt.AlignCenter:
            btn2.setChecked(True)
            btn2.setStyleSheet('background-color: #B7ECFF')
        else:
            btn1.setChecked(True)
            btn1.setStyleSheet('background-color: #B7ECFF')


if __name__ == '__main__':
    app = QApplication([])
    window = Notepad()
    window.show()
    exit(app.exec())
