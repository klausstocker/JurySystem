# Jurysystem
## Datenstruktur

```mermaid
erDiagram
    user (team) ||--o{ athletes : "consists of"
    athletes ||--o{ attendances : "attends"
    events ||--o{ attendances: "is attended"
    events ||--o{ eventCategories : "is categorized"
    events ||--o{ eventDiscipline : "consists of"
    rating ||--o{ eventDiscipline : ""
    attendances ||--o{ rating : "is rated"
    rating ||--o{ eventCategories : ""
    user (judge) ||--o{ ratings : "rates"
```