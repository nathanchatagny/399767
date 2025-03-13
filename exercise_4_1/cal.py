import datetime

class Cal:
    def __init__(self):
        # Initialisation avec l'année et le mois actuels pour que l'utilisateur 
        # n'ait pas besoin de les spécifier s'il veut le calendrier du mois en cours
        self._year = datetime.datetime.now().year
        self._month = datetime.datetime.now().month
        
        # Définit le début de la semaine à lundi (0) par défaut, conformément à la norme ISO
        # Cette valeur de décalage sera utilisée pour réorganiser l'affichage des jours
        self._week_start = 0
        
        # Dictionnaires de conversion pour permettre une interface flexible
        # Accepter plusieurs formats de saisie améliore l'expérience utilisateur
        self._month_dict = {
            "jan": 1, "january": 1, 
            "feb": 2, "february": 2,
            "mar": 3, "march": 3, 
            "apr": 4, "april": 4,
            "may": 5, 
            "jun": 6, "june": 6,
            "jul": 7, "july": 7, 
            "aug": 8, "august": 8,
            "sep": 9, "september": 9, 
            "oct": 10, "october": 10,
            "nov": 11, "november": 11,
            "dec": 12, "december": 12
        }
        self._day_dict = {
            "mon": 0, "monday": 0,
            "tue": 1, "tuesday": 1,
            "wed": 2, "wednesday": 2,
            "thu": 3, "thursday": 3,
            "fri": 4, "friday": 4,
            "sat": 5, "saturday": 5,
            "sun": 6, "sunday": 6
        }

    def year(self, year):
        # Méthode simple pour définir l'année
        # Retourne self pour permettre le chaînage des méthodes (pattern fluent interface)
        self._year = year
        return self
    
    def month(self, month):
        # Convertit le mois en nombre si c'est une chaîne
        # Cette flexibilité permet à l'utilisateur d'utiliser soit des nombres, soit des noms
        if isinstance(month, str):
            month = month.lower()  # Normalisation pour insensibilité à la casse
            if month in self._month_dict:
                self._month = self._month_dict[month]
            else:
                # Lever une exception est préférable à un comportement silencieux en cas d'erreur
                raise ValueError(f"Mois invalide: {month}")
        else:
            self._month = month
        return self
    
    def week_start(self, day):
        # Convertit le jour de début de semaine en décalage
        # Cette personnalisation permet d'adapter l'affichage aux conventions régionales
        day = day.lower()  # Normalisation pour une interface plus tolérante
        if day in self._day_dict:
            self._week_start = self._day_dict[day]
        else:
            raise ValueError(f"Jour de début de semaine invalide: {day}")
        return self
    
    def print(self):
        # Noms des mois pour l'affichage
        # Utilisation des noms complets pour une meilleure lisibilité
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        
        # Jours de la semaine ordonnés selon le jour de début
        # La rotation garantit que l'affichage commence par le jour choisi
        days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        weekdays = days[self._week_start:] + days[:self._week_start]
        
        # Affiche l'en-tête du calendrier
        # Formatage centré pour un affichage esthétique
        print(f"    {month_names[self._month-1]} {self._year}")
        print(" ".join(weekdays))
        
        # Calcule le premier jour du mois
        # Détermine où commencer l'affichage du calendrier
        first_day = datetime.datetime(self._year, self._month, 1)
        weekday = (first_day.weekday() - self._week_start) % 7
        
        # Calcule le dernier jour du mois
        # Gestion spéciale pour décembre pour éviter les problèmes de limite d'année
        if self._month == 12:
            last_day = datetime.datetime(self._year + 1, 1, 1) - datetime.timedelta(days=1)
        else:
            last_day = datetime.datetime(self._year, self._month + 1, 1) - datetime.timedelta(days=1)
        last_date = last_day.day
        
        # Construit les lignes du calendrier
        # Ajoute des espaces pour aligner correctement le premier jour
        line = ["  "] * weekday
        day = 1
        
        while day <= last_date:
            # Formatage à 2 caractères pour garantir l'alignement des colonnes
            line.append(f"{day:2d}")
            day += 1
            
            if len(line) == 7:
                # Imprime une ligne complète de la semaine
                print(" ".join(line))
                line = []
        
        # Imprime la dernière ligne si nécessaire
        # Complète avec des espaces pour maintenir l'alignement
        if line:
            line += ["  "] * (7 - len(line))
            print(" ".join(line))
        
        # Ligne vide à la fin pour meilleure lisibilité
        print()

c = Cal()
c.year(2025)
c.month("jan")
c.week_start("sun")
c.print()

c = Cal()
c.month("aug")
c.year(2025)
c.print()