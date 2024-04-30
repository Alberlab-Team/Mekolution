import sys
import json
from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, 
                               QListWidget, QLineEdit, QFileDialog, QInputDialog, QLabel, QHBoxLayout,
                               QDialog, QCheckBox)
from PySide6.QtGui import QIcon, QFont, QPainter, QBrush, QColor, QPalette
from PySide6.QtCore import Qt, QRect, QSize

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
        # Widgets pour l'édition JSON
        self.textEdit = QTextEdit()
        self.textEdit.setStyleSheet("border-radius: 10px; background-color: #F5F5F5;")
        self.keyList = QListWidget()
        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText('Rechercher une clé...')
        self.searchBar.textChanged.connect(self.searchKey)
        self.setWindowIcon(QIcon('source/picture/icon/icon_settings.png'))
        # Boutons
        self.loadButton = QPushButton('Charger JSON')
        self.loadButton.clicked.connect(self.loadJson)
        self.saveButton = QPushButton('Sauvegarder JSON')
        self.saveButton.clicked.connect(self.saveJson)
        self.editButton = QPushButton('Changer la valeur')
        self.editButton.clicked.connect(self.editValue)

        # Style des boutons
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
        # Style de QListWidget
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
        # Style de la barre de recherche pour arrondir les bords, l'agrandir et changer la couleur de fond
        self.searchBar.setStyleSheet("""
        QLineEdit {
            border-radius: 15px;
            padding: 10px;
            font-size: 16px; /* Ajustez la taille selon vos besoins */
            background-color: white;
        }
        """)
        self.keyList.setStyleSheet("""
        QListWidget {
            font-size: 18px; /* Ajustez la taille selon vos besoins */
            border-radius: 10px;
            background-color: #F0F0F0;
            color: #333;
        }
        QListWidget::item:selected {
            background-color: #9E9E9E;
            color: white;
        }
        """)

        # Appliquer le style à keyList
        self.keyList.setStyleSheet(list_style)
        # Appliquer le style aux boutons
        self.loadButton.setStyleSheet(button_style)
        self.saveButton.setStyleSheet(button_style)
        self.editButton.setStyleSheet(button_style)

        # Agrandir le texte dans QTextEdit
        self.textEdit.setStyleSheet("font-size: 16px; border-radius: 10px; background-color: #F5F5F5;")
        # Disposition
        layout = QVBoxLayout()
        layout.addWidget(self.searchBar)
        layout.addWidget(self.keyList)
        layout.addWidget(self.textEdit)
        layout.addWidget(self.loadButton)
        layout.addWidget(self.saveButton)
        layout.addWidget(self.editButton)

        # Widget central
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        # Style et géométrie
        self.setStyleSheet("background-color: #E0E0E0;")
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Editeur de paramètres - Settings editor')

    def loadJson(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Ouvrir fichier JSON", "", "JSON Files (*.json)")
        if fileName:
            with open(fileName, 'r', encoding='utf-8') as file:
                self.jsonObject = json.load(file)
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

            label = QLabel(key)
            label.setFont(QFont("Arial", 12))
            dialog_layout.addWidget(label)

            if isinstance(current_value, dict):
                dialog.setWindowTitle("Edit Dictionary")
                for sub_key, sub_value in current_value.items():
                    sub_dialog_layout = QHBoxLayout()
                    sub_label = QLabel(sub_key)
                    sub_label.setFont(QFont("Arial", 10))
                    sub_dialog_layout.addWidget(sub_label)
                    if isinstance(sub_value, bool):
                        checkbox = QCheckBox()
                        checkbox.setChecked(sub_value)
                        sub_dialog_layout.addWidget(checkbox)
                    else:
                        input_field = QLineEdit(str(sub_value))
                        input_field.setStyleSheet("border: 2px solid #4CAF50; border-radius: 5px;")
                        sub_dialog_layout.addWidget(input_field)
                    dialog_layout.addLayout(sub_dialog_layout)
            elif isinstance(current_value, bool):
                checkbox = QCheckBox()
                checkbox.setChecked(current_value)
                dialog_layout.addWidget(checkbox)
            else:
                input_field = QLineEdit(str(current_value))
                input_field.setStyleSheet("border: 2px solid #4CAF50; border-radius: 5px;")
                dialog_layout.addWidget(input_field)

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

    def saveValue(self, dialog, key, current_value):
        new_value = None
        if isinstance(current_value, dict):
            new_value = {}
            for i in range(dialog.layout().count() - 1):  # Exclude button layout
                sub_layout = dialog.layout().itemAt(i).layout()
                if sub_layout is not None:
                    sub_key = sub_layout.itemAt(0).widget().text()
                    if isinstance(current_value[sub_key], bool):
                        new_value[sub_key] = sub_layout.itemAt(1).widget().isChecked()
                    else:
                        new_value[sub_key] = sub_layout.itemAt(1).widget().text()
        elif isinstance(current_value, bool):
            new_value = dialog.layout().itemAt(1).widget().isChecked()
        else:
            new_value = dialog.layout().itemAt(1).widget().text()
        self.jsonObject[key] = new_value
        self.textEdit.setText(json.dumps(self.jsonObject, indent=4))
        dialog.close()

    def populateList(self):
        self.keyList.clear()
        for key in self.jsonObject.keys():
            self.keyList.addItem(key)

app = QApplication(sys.argv)
editor = JsonEditor()
editor.show()
sys.exit(app.exec_())
