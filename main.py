import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QLabel, QTextEdit,
    QLineEdit, QMessageBox
)
import data_processor
from analyse import AnalyseComparaison

class PMUInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialisation de l'interface graphique."""
        self.setWindowTitle("Logiciel PMU - Comparaison Equidia/Zeturf")
        self.setGeometry(100, 100, 1200, 600)

        layout = QVBoxLayout()

        # Champ pour coller les infos Equidia
        self.equidia_label = QLabel("Collez ici les informations Equidia :")
        layout.addWidget(self.equidia_label)
        self.equidia_text_edit = QTextEdit()
        layout.addWidget(self.equidia_text_edit)

        # Champ pour coller les numéros Zeturf
        self.zeturf_label = QLabel("Collez ici les numéros de Zeturf (ex: 16 - 11 - 7 - 12) :")
        layout.addWidget(self.zeturf_label)
        self.zeturf_input = QLineEdit()
        layout.addWidget(self.zeturf_input)

        # Zone pour coller les données PMU
        self.label = QLabel("Copiez-collez les données PMU ici :")
        layout.addWidget(self.label)
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        # Bouton pour traiter les données
        self.process_button = QPushButton("Traiter les données")
        self.process_button.clicked.connect(self.process_data)
        layout.addWidget(self.process_button)

        # Bouton pour analyse comparée
        self.analyse_comparaison_button = QPushButton("Analyse Comparée")
        self.analyse_comparaison_button.clicked.connect(self.ouvrir_analyse_comparaison)
        layout.addWidget(self.analyse_comparaison_button)

        # Tableau des résultats
        self.result_label = QLabel("Tableau des résultats :")
        layout.addWidget(self.result_label)

        self.table = QTableWidget()
        self.table.setColumnCount(14)
        self.table.setHorizontalHeaderLabels([
            "Numéro", "Nom du Cheval", "Jockey & Entraîneur", "Sexe", "Âge",
            "Distance", "Chrono", "Gains", "Performances",
            "E-Bases", "E-Outsiders", "E-Belles chances", "E-Délaissés", "Zeturf"
        ])
        layout.addWidget(self.table)

        self.setLayout(layout)

    def process_data(self):
        """Récupère les données et les affiche sous forme de tableau."""
        raw_text = self.text_edit.toPlainText()
        equidia_text = self.equidia_text_edit.toPlainText()
        zeturf_text = self.zeturf_input.text()

        if not raw_text.strip():
            self.result_label.setText("Aucune donnée PMU à traiter.")
            return

        # Extraction et traitement des données
        self.parsed_data = data_processor.parse_pmu_data(raw_text)
        self.equidia_selection = data_processor.extract_selection_data(equidia_text)
        self.zeturf_selection = data_processor.extract_zeturf_data(zeturf_text)

        # Remplir le tableau
        self.populate_table(self.parsed_data, self.equidia_selection, self.zeturf_selection)

    def populate_table(self, data, equidia_data, zeturf_numbers):
        """Remplit le tableau avec les données traitées et les sélections Equidia/Zeturf."""
        self.table.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            numero = str(row_data[0])  # Convertir en chaîne pour comparer correctement
            for col_idx, cell in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(cell))

            # Ajouter les sélections Equidia
            self.table.setItem(row_idx, 9, QTableWidgetItem("✅" if numero in equidia_data.get("Bases", []) else ""))
            self.table.setItem(row_idx, 10, QTableWidgetItem("✅" if numero in equidia_data.get("Outsiders", []) else ""))
            self.table.setItem(row_idx, 11, QTableWidgetItem("✅" if numero in equidia_data.get("Belles chances", []) else ""))
            self.table.setItem(row_idx, 12, QTableWidgetItem(numero if numero in equidia_data.get("Délaissés", []) else ""))

            # Ajouter les sélections Zeturf
            self.table.setItem(row_idx, 13, QTableWidgetItem("✅" if numero in zeturf_numbers else ""))

    def ouvrir_analyse_comparaison(self):
        """Ouvre la fenêtre d'analyse comparée avec les musiques et les délaissés."""
        if not hasattr(self, 'equidia_selection') or not hasattr(self, 'zeturf_selection') or not hasattr(self, 'parsed_data'):
            QMessageBox.warning(self, "Analyse impossible", "Veuillez d'abord traiter les données PMU.")
            return

        # Récupérer les délaissés
        delaisses = self.equidia_selection.get("Délaissés", [])

        self.analyse_fenetre = AnalyseComparaison(
            self.equidia_selection.get("Bases", []) + self.equidia_selection.get("Outsiders", []) + self.equidia_selection.get("Belles chances", []),
            self.zeturf_selection,
            [row[0] for row in self.parsed_data],  # Liste des numéros des chevaux
            self.parsed_data,  # On passe les données complètes pour récupérer les musiques
            delaisses  # On passe maintenant les délaissés !
        )
        self.analyse_fenetre.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PMUInterface()
    window.show()
    sys.exit(app.exec())