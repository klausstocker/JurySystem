# Jurysystem
## Datenstruktur

```mermaid
erDiagram
    user ||--o| teams: "manages"
    teams ||--o{ athletes : "consists of"
    athletes ||--o{ attendances : "attends"
    competitions ||--o{ attendances: "is attended"
    competitions ||--o{ competitionCategories : "is categorized"
    discipline ||--o{ competiotionDiscipline : ""
    rating ||--o{ competiotionDiscipline :""
    attendances ||--o{ rating : ""
    rating ||--o{ competitionCategories : ""
```