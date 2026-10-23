# Jurysystem
## Datenstruktur

```mermaid
erDiagram
    users {
        int(10) id PK "unsigned"
        varchar(50) username UK
        varchar(500) hash
        varchar(50) email
        varchar(50) team
        datetime registered
        datetime expires
        tinyint(4) restrictions
        tinyint(4) locked
        tinyint(4) hidden
        varchar(50) token
        varchar(2) language
    }

    athletes {
        int(10) id PK "unsigned"
        varchar(50) givenname
        varchar(50) surname
        int(10) userId FK "unsigned"
        datetime birth
        tinyint(4) gender
        tinyint(4) hidden
    }

    events {
        int(10) id PK "unsigned"
        varchar(50) name
        int(10) userId FK "unsigned"
        datetime date
        tinyint(4) finished
        tinyint(4) deleted
        varchar(500) customRanking
    }

    event_judges {
        int(10) eventId PK, FK "unsigned"
        int(10) userId PK, FK "unsigned"
    }

    event_categories {
        varchar(50) name PK
        int(10) eventId PK, FK "unsigned"
        tinyint(4) gender
        datetime birthFrom
        datetime birthTo
        tinyint(4) rankingType
        varchar(500) rankingAlgo
    }

    event_disciplines {
        varchar(50) name PK
        int(10) eventId PK, FK "unsigned"
    }

    attendances {
        int(10) athleteId PK, FK "unsigned"
        int(10) eventId PK, FK "unsigned"
        varchar(50) eventCategoryName PK
        varchar(50) group
        tinyint(4) hidden
    }

    ratings {
        int(10) id PK "unsigned"
        datetime ts
        int(10) athleteId FK, UK "unsigned"
        varchar(50) eventDisciplineName UK
        int(10) eventId FK, UK "unsigned"
        int(10) userId FK "unsigned"
        decimal(8,4) difficulty
        decimal(8,4) execution
    }

    users ||..o{ athletes : "has team members"
    users ||..o{ events : "organizes"
    users ||--o{ event_judges : "judges at"
    users ||..o{ ratings : "rates"
    events ||--o{ event_judges : "has judges"
    events ||--o{ event_categories : "has categories"
    events ||--o{ event_disciplines : "has disciplines"
    events ||--o{ attendances : "has participants"
    athletes ||--o{ attendances : "attends"
    events ||..o{ ratings : "has ratings"
    athletes ||..o{ ratings : "receives"
```

Das Diagramm zeigt die in `docker-entrypoint-initdb.d/init.sql` definierten Tabellen und Fremdschlüsselbeziehungen. Durchgezogene Linien kennzeichnen Beziehungen, bei denen der Fremdschlüssel Teil des Primärschlüssels ist; gestrichelte Linien kennzeichnen die übrigen Beziehungen.

Mehrere `PK`-Attribute einer Tabelle bilden zusammen den Primärschlüssel. In `ratings` bilden die drei `UK`-Attribute gemeinsam den eindeutigen Schlüssel (`athleteId`, `eventId`, `eventDisciplineName`).

Für `attendances.eventCategoryName` und `ratings.eventDisciplineName` sind in `init.sql` keine Fremdschlüssel auf `event_categories` bzw. `event_disciplines` definiert. Auch zwischen `ratings` und `attendances` besteht kein definierter Fremdschlüssel.
