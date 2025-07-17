# Jurysystem
## Datenstruktur

```mermaid
erDiagram
    users (team) ||--o{ athletes : "consists of"
    athletes ||--o{ attendances : "attends"
    events ||--o{ attendances: "is attended"
    events ||--o{ eventCategories : "is categorized"
    events ||--o{ eventDiscipline : "consists of"
    events ||--o{ event_judges : "are visited by"
    users (only judge) ||--o{ event_judges : "judge at"
    rating ||--o{ eventDiscipline : ""
    attendances ||--o{ rating : "is rated"
    rating ||--o{ eventCategories : ""
    users (judge) ||--o{ ratings : "rates"
```