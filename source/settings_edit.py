import sys
import json
from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, 
                               QListWidget, QLineEdit, QFileDialog, QLabel, QHBoxLayout, QDialog, QCheckBox)
from PySide6.QtGui import QIcon, QFont, QPainter, QBrush, QColor
from PySide6.QtCore import Qt, QRect


class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Dictionary")
        self.setStyleSheet("background-color: #F5F5F5; border-radius: 10px;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        brush = QBrush(QColor("#F5F5F5"))
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)

        rect = QRect(0, 0, self.width(), self.height())
        painter.drawRoundedRect(rect, 10, 10)


class JsonEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.jsonObject = None
        self.initUI()

    def initUI(self):
        self.textEdit = QTextEdit()
        self.textEdit.setStyleSheet("border-radius: 10px; background-color: #F5F5F5;")
        self.keyList = QListWidget()
        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText('Rechercher une clé...')
        self.searchBar.textChanged.connect(self.searchKey)
        self.setWindowIcon(QIcon('source/picture/icon/icon_settings.png'))

        self.NewSheetButton = QPushButton('Créer une nouvelle setting sheet')
        self.NewSheetButton.clicked.connect(self.NewJson)

        self.loadButton = QPushButton('Charger une setting sheet')
        self.loadButton.clicked.connect(self.loadJson)

        self.saveButton = QPushButton('Sauvegarder la setting sheet')
        self.saveButton.clicked.connect(self.saveJson)

        self.editButton = QPushButton('Changer la valeur')
        self.editButton.clicked.connect(self.editValue)

        button_style = """
        QPushButton {
            border-radius: 15px;
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            margin: 10px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        """

        list_style = """
        QListWidget {
            font-size : 18px;
            border-radius: 10px;
            background-color: #F0F0F0;
            color: #333;
        }
        QListWidget::item:selected {
            background-color: #4CAF50;
            color: white;
        }
        """

        self.searchBar.setStyleSheet("""
        QLineEdit {
            border-radius: 15px;
            padding: 10px;
            font-size: 16px;
            background-color: white;
        }
        """)

        self.keyList.setStyleSheet(list_style)
        self.NewSheetButton.setStyleSheet(button_style)
        self.loadButton.setStyleSheet(button_style)
        self.saveButton.setStyleSheet(button_style)
        self.editButton.setStyleSheet(button_style)

        self.textEdit.setStyleSheet("font-size: 16px; border-radius: 10px; background-color: #F5F5F5;")

        layout = QVBoxLayout()
        layout.addWidget(self.searchBar)
        layout.addWidget(self.keyList)
        layout.addWidget(self.textEdit)
        layout.addWidget(self.NewSheetButton)
        layout.addWidget(self.loadButton)
        layout.addWidget(self.saveButton)
        layout.addWidget(self.editButton)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        self.setStyleSheet("background-color: #E0E0E0;")
        self.setGeometry(0, 0, *QApplication.primaryScreen().size().toTuple())
        self.setWindowTitle('Editeur de paramètres - Settings editor')

    def NewJson(self):
        dirPath = QFileDialog.getExistingDirectory(self, "Choisir un dossier")
        with open("source/config/pack1/jsonbasecontent.json", "r") as pack1:
            basecontent = pack1.read()
        with open(f"{dirPath}/settings.json", "w+") as jsonfile:
            jsonfile.write(basecontent)

    def loadJson(self, isNew=False, file=None):
        with open("source/config/pack1/jsonbasecontent.json", "r") as pack1:
            baseSettings: dict = json.load(pack1)
        Settings = {}
        fileName = True
        while list(baseSettings.keys()) != list(Settings.keys()) and fileName:
            fileName, _ = QFileDialog.getOpenFileName(self, "Ouvrir fichier JSON", "", "JSON Files (*.json)")
            if fileName:
                with open(fileName, 'r', encoding='utf-8') as file:
                    Settings = json.load(file)
        with open('TempVar.json', 'r') as File:
            Globalr = json.load(File)
            Globalr['setting_sheet_path'] = fileName
            with open('TempVar.json', 'w') as Globalw:
                json.dump(Globalr, Globalw)
        if fileName:
            self.jsonObject = Settings
            self.textEdit.setText(json.dumps(self.jsonObject, indent=4))
            self.populateList()

    def saveJson(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Sauvegarder fichier JSON", "", "JSON Files (*.json)")
        if fileName:
            with open(fileName, 'w', encoding='utf-8') as file:
                json.dump(self.jsonObject, file, indent=4)

    def searchKey(self):
        searchTerm = self.searchBar.text().lower()
        for i in range(self.keyList.count()):
            if searchTerm in self.keyList.item(i).text().lower():
                self.keyList.item(i).setSelected(True)
            else:
                self.keyList.item(i).setSelected(False)

    def editValue(self):
        selectedItems = self.keyList.selectedItems()
        if selectedItems:
            key = selectedItems[0].text()
            current_value = self.jsonObject[key]
            dialog = Dialog()
            dialog.setWindowTitle(f"Changer la valeur pour {key}")
            dialog_layout = QVBoxLayout(dialog)

            self.createDialogLayout(dialog_layout, current_value)

            button_layout = QHBoxLayout()
            save_button = QPushButton("Save")
            save_button.setStyleSheet("border: 2px solid #4CAF50; border-radius: 5px;")
            save_button.clicked.connect(lambda: self.saveValue(dialog, key, current_value))
            button_layout.addWidget(save_button)

            cancel_button = QPushButton("Cancel")
            cancel_button.setStyleSheet("border: 2px solid #4CAF50; border-radius: 5px;")
            cancel_button.clicked.connect(dialog.close)
            button_layout.addWidget(cancel_button)

            dialog_layout.addLayout(button_layout)
            dialog.setLayout(dialog_layout)
            dialog.exec_()

    def createDialogLayout(self, layout, current_value):
        current_value_type = type(current_value)

        if current_value_type == dict:
            for sub_key, sub_value in current_value.items():
                sub_value_type = type(sub_value)
                sub_dialog_layout = QVBoxLayout()
                sub_label = QLabel(sub_key)
                sub_label.setFont(QFont("Arial", 10))
                sub_dialog_layout.addWidget(sub_label)
                if sub_value_type == bool:
                    checkbox = QCheckBox()
                    checkbox.setChecked(sub_value)
                    sub_dialog_layout.addWidget(checkbox)
                elif sub_value_type in [str, int, float]:
                    input_field = QLineEdit(str(sub_value))
                    input_field.setStyleSheet("border: 2px solid #4CAF50; border-radius: 5px;")
                    sub_dialog_layout.addWidget(input_field)
                elif sub_value_type == dict:
                    self.createDialogLayout(sub_dialog_layout, sub_value)
                layout.addLayout(sub_dialog_layout)

        elif current_value_type == bool:
            checkbox = QCheckBox()
            checkbox.setChecked(current_value)
            layout.addWidget(checkbox)

        elif current_value_type in [int, float, str]:
            input_field = QLineEdit(str(current_value))
            input_field.setStyleSheet("border: 2px solid #4CAF50; border-radius: 5px;")
            layout.addWidget(input_field)

    def saveValue(self, dialog, key, current_value):

        def saveIntFloatOrStr(layout):
            widget = layout.itemAt(1).widget()
            if widget:
                new_value = widget.text()
                try:
                    new_value = int(new_value)
                except ValueError:
                    try:
                        new_value = float(new_value)
                    except ValueError:
                        pass
                return new_value
            return None

        def saveBool(layout):
            widget = layout.itemAt(1).widget()
            if widget:
                return widget.isChecked()
            return None

        def saveDict(layout, current_dict):
            new_dict = {}
            for i in range(layout.count()):
                sub_layout = layout.itemAt(i).layout()
                if sub_layout and sub_layout.itemAt(0).widget() and isinstance(sub_layout.itemAt(0).widget(), QLabel):
                    sub_key = sub_layout.itemAt(0).widget().text()
                    sub_value = current_dict.get(sub_key, None)
                    sub_value_type = type(sub_value)
                    if sub_value_type == bool:
                        new_dict[sub_key] = saveBool(sub_layout)
                    elif sub_value_type in [str, int, float]:
                        new_dict[sub_key] = saveIntFloatOrStr(sub_layout)
                    elif sub_value_type == dict:
                        new_dict[sub_key] = saveDict(sub_layout, sub_value)
            return new_dict

        new_value = None
        value_type = type(current_value)

        if value_type == dict:
            new_value = saveDict(dialog.layout(), current_value)

        elif value_type == bool:
            new_value = saveBool(dialog.layout())

        elif value_type in [str, int, float]:
            new_value = saveIntFloatOrStr(dialog.layout())

        self.jsonObject[key] = new_value
        self.textEdit.setText(json.dumps(self.jsonObject, indent=4))
        dialog.close()

    def populateList(self):
        self.keyList.clear()
        for key in self.jsonObject.keys():
            self.keyList.addItem(key)


def settings(app : QApplication | None = None)->QApplication:
    if app is None:
        app = QApplication(sys.argv)
    editor = JsonEditor()
    editor.show()
    app.exec()
    editor.close()
    return app


#settings()
