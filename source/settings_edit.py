# SkyDev

import sys
import json
from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, 
                               QListWidget, QLineEdit, QMessageBox, QFileDialog, QInputDialog)
from PySide6.QtGui import QIcon

def settings():
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

            # Style de la barre de recherche pour arrondir les bords, l'agrandir et changer la couleur de fond
            self.searchBar.setStyleSheet("""
            QLineEdit {
                border-radius: 15px;
                padding: 10px;
                font-size: 16px; /* Ajustez la taille selon vos besoins */
                background-color: white;
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
                value, ok = QInputDialog.getText(self, f"Changer la valeur pour {key}", "Entrer la nouvelle valeur:")
                if ok and value:
                    try:
                        # Évaluer la valeur pour conserver le type de données correct
                        evaluated_value = json.loads(value)
                    except json.JSONDecodeError:
                        # Si l'évaluation échoue, traiter comme une chaîne de caractères
                        evaluated_value = value
                    self.jsonObject[key] = evaluated_value
                    self.textEdit.setText(json.dumps(self.jsonObject, indent=4))

        def populateList(self):
            self.keyList.clear()
            for key in self.jsonObject.keys():
                self.keyList.addItem(key)

    app = QApplication(sys.argv)
    editor = JsonEditor()
    editor.show()
    sys.exit(app.exec())

