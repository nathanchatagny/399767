import unittest
from unittest.mock import patch
import datetime
from cal import Cal
import io
import sys

class TestCal(unittest.TestCase):
    
    def setUp(self):
        # Création d'une instance fraîche pour chaque test pour éviter les effets de bord
        # Les tests unitaires doivent être indépendants les uns des autres
        self.cal = Cal()
    
    def test_init_defaults(self):
        # Test des valeurs par défaut lors de l'initialisation
        # Ceci est important car le comportement par défaut doit être prévisible
        today = datetime.datetime.now()
        self.assertEqual(self.cal._year, today.year)
        self.assertEqual(self.cal._month, today.month)
        self.assertEqual(self.cal._week_start, 0)  # Lundi par défaut
    
    def test_year_method(self):
        # Vérifie que la méthode year modifie correctement l'année
        # Le pattern fluent (chaînage de méthodes) nécessite que chaque méthode retourne self
        result = self.cal.year(2024)
        self.assertEqual(self.cal._year, 2024)
        self.assertEqual(result, self.cal)  # Test du retour de self pour le chaînage
    
    def test_month_numeric(self):
        # Test avec une valeur numérique pour le mois
        # Vérifie que l'entrée numérique fonctionne correctement
        result = self.cal.month(4)
        self.assertEqual(self.cal._month, 4)
        self.assertEqual(result, self.cal)  # Vérifie le chaînage
    
    def test_month_string_full(self):
        # Test avec le nom complet du mois
        # Cela garantit que l'interface utilisateur est flexible
        result = self.cal.month("January")
        self.assertEqual(self.cal._month, 1)
        self.assertEqual(result, self.cal)
    
    def test_month_string_abbreviated(self):
        # Test avec l'abréviation du mois
        # L'utilisateur doit pouvoir utiliser différents formats
        result = self.cal.month("feb")
        self.assertEqual(self.cal._month, 2)
        self.assertEqual(result, self.cal)
    
    def test_month_case_insensitive(self):
        # Test de l'insensibilité à la casse
        # Le code doit être tolérant aux variations de casse pour une meilleure UX
        result = self.cal.month("MaRcH")
        self.assertEqual(self.cal._month, 3)
        self.assertEqual(result, self.cal)
    
    def test_month_invalid(self):
        # Test avec un mois invalide
        # La validation des entrées est essentielle pour une utilisation robuste
        with self.assertRaises(ValueError):
            self.cal.month("invalid_month")
    
    def test_week_start(self):
        # Test du réglage du jour de début de semaine
        # Cette flexibilité permet d'adapter l'affichage selon les préférences régionales
        result = self.cal.week_start("sun")
        self.assertEqual(self.cal._week_start, 6)
        self.assertEqual(result, self.cal)
    
    def test_week_start_invalid(self):
        # Test avec un jour de début de semaine invalide
        # Validation nécessaire pour éviter les erreurs silencieuses
        with self.assertRaises(ValueError):
            self.cal.week_start("invalid_day")
    
    def test_print_output(self):
        # Test de la sortie générée par print()
        # Capture la sortie standard pour la vérifier
        # La sortie visuelle est l'élément principal de cette classe
        self.cal.year(2025).month(2).week_start("mon")
        
        # Redirection de stdout pour capture
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        self.cal.print()
        
        # Restauration de stdout
        sys.stdout = sys.__stdout__
        
        # Ajustement pour correspondre à la sortie réelle avec espaces à la fin des lignes
        expected_output = """    February 2025
Mo Tu We Th Fr Sa Su
                1  2
 3  4  5  6  7  8  9
10 11 12 13 14 15 16
17 18 19 20 21 22 23
24 25 26 27 28      

"""
        self.assertEqual(captured_output.getvalue(), expected_output)
    
    def test_print_with_sunday_start(self):
        # Test avec dimanche comme premier jour de la semaine
        # Vérifie que le décalage des jours fonctionne correctement
        self.cal.year(2025).month(2).week_start("sun")
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        self.cal.print()
        
        sys.stdout = sys.__stdout__
        
        # Ajustement pour correspondre à la sortie réelle avec espaces à la fin des lignes
        expected_output = """    February 2025
Su Mo Tu We Th Fr Sa
                   1
 2  3  4  5  6  7  8
 9 10 11 12 13 14 15
16 17 18 19 20 21 22
23 24 25 26 27 28   

"""
        self.assertEqual(captured_output.getvalue(), expected_output)
    
    def test_print_month_with_31_days(self):
        # Test avec un mois de 31 jours
        # Vérifie que la classe gère correctement les mois de différentes longueurs
        self.cal.year(2025).month(1).week_start("mon")
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        self.cal.print()
        
        sys.stdout = sys.__stdout__
        
        # Vérification que le mois complet est affiché
        self.assertIn("31", captured_output.getvalue())
    
    def test_print_december_to_january_transition(self):
        # Test de la transition décembre à janvier
        # Vérifie que le calcul du dernier jour fonctionne correctement lors du changement d'année
        self.cal.year(2024).month(12).week_start("mon")
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        self.cal.print()
        
        sys.stdout = sys.__stdout__
        
        # Vérification que le mois complet est affiché
        self.assertIn("31", captured_output.getvalue())
    
    @patch('datetime.datetime')
    def test_init_with_mocked_date(self, mock_datetime):
        # Test avec une date système simulée
        # Utilise le mocking pour garantir un comportement prévisible indépendamment de la date d'exécution
        mock_now = unittest.mock.MagicMock()
        mock_now.year = 2023
        mock_now.month = 5
        mock_datetime.now.return_value = mock_now
        
        cal = Cal()
        
        self.assertEqual(cal._year, 2023)
        self.assertEqual(cal._month, 5)

if __name__ == '__main__':
    unittest.main()