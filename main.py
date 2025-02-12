import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QLabel, QTextEdit,
    QLineEdit, QMessageBox
)
import data_processor


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
        self.zeturf_input = QLineEdit()  # Champ simplifié pour Zeturf
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

        # Tableau des résultats
        self.result_label = QLabel("Tableau des résultats :")
        layout.addWidget(self.result_label)

        self.table = QTableWidget()
        self.table.setColumnCount(14)  # Ajout d'une colonne pour "E-Délaissés"
        self.table.setHorizontalHeaderLabels([
            "Numéro", "Nom du Cheval", "Jockey & Entraîneur", "Sexe", "Âge",
            "Distance", "Chrono", "Gains", "Performances",
            "E-Bases", "E-Outsiders", "E-Belles chances", "E-Délaissés", "Zeturf"
        ])
        layout.addWidget(self.table)

        # Bouton pour analyser le tableau
        self.analyse_button = QPushButton("Analyser le Tableau")
        self.analyse_button.clicked.connect(self.analyser_tableau)
        layout.addWidget(self.analyse_button)

        self.setLayout(layout)

    def process_data(self):
        """Récupère les données et les affiche sous forme de tableau."""
        raw_text = self.text_edit.toPlainText()
        equidia_text = self.equidia_text_edit.toPlainText()
        zeturf_text = self.zeturf_input.text()  # Zeturf est maintenant un champ simplifié

        print("📌 Contenu brut des données Equidia :", repr(equidia_text))  # Debugging

        if not raw_text.strip():
            self.result_label.setText("Aucune donnée PMU à traiter.")
            return

        parsed_data = data_processor.parse_pmu_data(raw_text)

        if not parsed_data:
            self.result_label.setText("Format invalide ! Vérifiez les données PMU.")
            return

        # Extraction des sélections Equidia
        equidia_data = data_processor.extract_selection_data(equidia_text)
        print("📌 Délaissés extraits après correction :", equidia_data.get("Délaissés", []))  # Debugging

        # Vérifier que la clé "Délaissés" existe, sinon l'ajouter
        if "Délaissés" not in equidia_data:
            equidia_data["Délaissés"] = []

        # Extraction des numéros de Zeturf
        zeturf_numbers = data_processor.extract_zeturf_data(zeturf_text)

        self.populate_table(parsed_data, equidia_data, zeturf_numbers)

    def populate_table(self, data, equidia_data, zeturf_numbers):
        """Remplit le tableau avec les données traitées et les sélections Equidia/Zeturf."""
        self.table.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            numero = row_data[0]

            for col_idx, cell in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(cell))

            # Ajouter les sélections Equidia
            self.table.setItem(row_idx, 9, QTableWidgetItem("✅" if numero in equidia_data.get("Bases", []) else ""))
            self.table.setItem(row_idx, 10,
                               QTableWidgetItem("✅" if numero in equidia_data.get("Outsiders", []) else ""))
            self.table.setItem(row_idx, 11,
                               QTableWidgetItem("✅" if numero in equidia_data.get("Belles chances", []) else ""))

            # Correction de l'affichage des Délaissés
            if "Délaissés" in equidia_data and numero in equidia_data["Délaissés"]:
                self.table.setItem(row_idx, 12, QTableWidgetItem(str(numero)))  # Afficher le numéro du cheval délaissé

            # Ajouter les sélections Zeturf
            self.table.setItem(row_idx, 13, QTableWidgetItem("✅" if numero in zeturf_numbers else ""))

    def analyser_tableau(self):
        """Analyse les résultats du tableau et affiche un résumé."""
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "Analyse impossible", "Le tableau est vide, aucune analyse possible.")
            return

        total_chevaux = self.table.rowCount()
        bases = sum(
            1 for row in range(total_chevaux) if self.table.item(row, 9) and self.table.item(row, 9).text() == "✅")
        outsiders = sum(
            1 for row in range(total_chevaux) if self.table.item(row, 10) and self.table.item(row, 10).text() == "✅")
        belles_chances = sum(
            1 for row in range(total_chevaux) if self.table.item(row, 11) and self.table.item(row, 11).text() == "✅")
        delaisses = sum(
            1 for row in range(total_chevaux) if self.table.item(row, 12) and self.table.item(row, 12).text() != "")
        zeturf_favoris = sum(
            1 for row in range(total_chevaux) if self.table.item(row, 13) and self.table.item(row, 13).text() == "✅")

        message = (
            f"📊 **Analyse du Tableau :**\n"
            f"- 🏇 Total Chevaux : {total_chevaux}\n"
            f"- 🔹 Bases Equidia : {bases}\n"
            f"- 🔸 Outsiders Equidia : {outsiders}\n"
            f"- ⭐ Belles Chances Equidia : {belles_chances}\n"
            f"- ⚫ Délaissés Equidia : {delaisses}\n"
            f"- 🔵 Favoris Zeturf : {zeturf_favoris}\n"
        )

        QMessageBox.information(self, "Analyse des Résultats", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PMUInterface()
    window.show()
    sys.exit(app.exec())