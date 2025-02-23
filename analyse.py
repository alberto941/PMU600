from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton


class AnalyseComparaison(QWidget):
    def __init__(self, equidia_data, zeturf_data, chevaux_liste):
        super().__init__()
        self.setWindowTitle("Analyse Comparée - Equidia & Zeturf")
        self.setGeometry(150, 150, 600, 400)

        layout = QVBoxLayout()

        # Chevaux choisis par les deux sites
        self.label_commun = QLabel("\u2705 Chevaux choisis par Equidia & Zeturf :")
        layout.addWidget(self.label_commun)
        self.list_commun = QListWidget()
        layout.addWidget(self.list_commun)

        # Chevaux choisis uniquement par Equidia
        self.label_equidia = QLabel("\ud83d\udfe6 Chevaux uniquement choisis par Equidia :")
        layout.addWidget(self.label_equidia)
        self.list_equidia = QListWidget()
        layout.addWidget(self.list_equidia)

        # Chevaux choisis uniquement par Zeturf
        self.label_zeturf = QLabel("\ud83d\udd35 Chevaux uniquement choisis par Zeturf :")
        layout.addWidget(self.label_zeturf)
        self.list_zeturf = QListWidget()
        layout.addWidget(self.list_zeturf)

        # Chevaux non choisis
        self.label_aucun = QLabel("⚪ Chevaux non sélectionnés par aucun des sites :")
        layout.addWidget(self.label_aucun)
        self.list_aucun = QListWidget()
        layout.addWidget(self.list_aucun)

        # Bouton de fermeture
        self.close_button = QPushButton("Fermer")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

        # Lancer l'analyse
        self.analyser_donnees(equidia_data, zeturf_data, chevaux_liste)

    def analyser_donnees(self, equidia_data, zeturf_data, chevaux_liste):
        """Analyse et affichage des chevaux dans les catégories correspondantes."""
        set_equidia = set(equidia_data)
        set_zeturf = set(zeturf_data)
        set_tous = set(chevaux_liste)

        # Chevaux choisis par les deux sites
        communs = set_equidia & set_zeturf
        self.list_commun.addItems([str(num) for num in sorted(communs)])

        # Chevaux uniquement choisis par Equidia
        seuls_equidia = set_equidia - set_zeturf
        self.list_equidia.addItems([str(num) for num in sorted(seuls_equidia)])

        # Chevaux uniquement choisis par Zeturf
        seuls_zeturf = set_zeturf - set_equidia
        self.list_zeturf.addItems([str(num) for num in sorted(seuls_zeturf)])

        # Chevaux non choisis
        non_choisis = set_tous - (set_equidia | set_zeturf)
        self.list_aucun.addItems([str(num) for num in sorted(non_choisis)])
