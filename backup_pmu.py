# Ton code actuel sauvegardé ici
# Tu pourras revenir à cette version si besoin

# Importation des modules nécessaires
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout


class PMUApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Logiciel PMU')
        layout = QVBoxLayout()

        self.btn_import = QPushButton('Importer Fichier Excel', self)
        layout.addWidget(self.btn_import)

        self.btn_select_favoris = QPushButton('Sélectionner les Favoris', self)
        layout.addWidget(self.btn_select_favoris)

        self.btn_optimiser = QPushButton('Optimiser les Combinaisons', self)
        layout.addWidget(self.btn_optimiser)

        self.btn_resultats = QPushButton('Afficher les Résultats', self)
        layout.addWidget(self.btn_resultats)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = PMUApp()
    mainWin.show()
    sys.exit(app.exec_())
