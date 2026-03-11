class tr:
    def __init__(self, language: str = 'en'):
        self.language = language

    translations = {
        'ge': {
            'Yes': 'Ja',
            'No': 'Nein',
            'given name': 'Vorname',
            'surname': 'Nachname',
            'team': 'Verein',
            'birth': 'Geburtsdatum',
            'gender': 'Geschlecht',
            'Edit': 'Editieren',
            'Delete': 'Löschen',
            'Add': 'Hinzufügen',
            'pick date': 'Datum wählen',
            'Save': 'Speichern',
            'Cancel': 'Abbrechen',
            'Delete athlete': 'Sportler löschen',
            'Help': 'Hilfe',
            'select event': 'wähle event',
            'Athletes': 'Sportler',
            'Attendances': 'Teilnahmen',
            'Rating': 'Bewertung',
            'Ranking': 'Ergebnisse',
            'Attendances of': 'Teilnahmen von',
            'category': 'Klasse',
            'group': 'Riege'
        }
    }

    def tr(self, english: str) -> str:
        if self.language == 'en':
            return english
        if self.language not in self.translations:
            return english
        if english not in self.translations[self.language]:
            print(f'missing translation for {english}')
            return english

        return self.translations[self.language][english]