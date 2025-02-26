from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton

class AnalyseComparaison(QWidget):
    def __init__(self, equidia_selection, zeturf_selection, chevaux_liste, parsed_data, delaisses):
        super().__init__()
        self.setWindowTitle("Analyse Comparée - Equidia & Zeturf")
        self.setGeometry(200, 200, 800, 600)

        layout = QVBoxLayout()

        def create_text_list(title, chevaux):
            label = QLabel(title)
            text_box = QTextEdit()
            text_box.setReadOnly(True)

            for numero in chevaux:
                musique = next((row[8] for row in parsed_data if str(row[0]) == str(numero)), "N/A")

                if musique.count("1") >= 2 or musique.count("2") >= 2:
                    note = "🟢 Bonne musique"
                elif musique.count("8") >= 2 or musique.count("9") >= 2:
                    note = "🔴 Mauvaise musique"
                else:
                    note = "⚪ Moyenne"

                text_box.append(f"{numero} - {musique} ({note})")

            layout.addWidget(label)
            layout.addWidget(text_box)

        create_text_list("✅ Chevaux choisis par Equidia & Zeturf :", list(set(equidia_selection) & set(zeturf_selection)))
        create_text_list("🔵 Chevaux uniquement choisis par Equidia :", list(set(equidia_selection) - set(zeturf_selection)))
        create_text_list("🔵 Chevaux uniquement choisis par Zeturf :", list(set(zeturf_selection) - set(equidia_selection)))
        create_text_list("⚪ Chevaux délaissés :", delaisses)

        close_button = QPushButton("Fermer")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)