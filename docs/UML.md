# UML Diagram
This file contains the UML diagram for the CASP-Data-Extractor

## PlantUML code
@startuml

enum Metrics {
- N1
- N2
- Dist
- N
- RMSD
- GDT_TS
- LGA_S3
- LGA_Q3
  }

struct Casp {
- name: str
- data_url: str
- winner: ?
- metric: [Metrics] // 1-8
- targets: [str] // amount of targets
- groups: HashMap[group_name: str, Group]
+ calculate_winner() -> ?
  }

struct Group {
- models: HashMap[target_name: str, List[Model]]
  }

struct Model {
- metrics: HashMap[Metrics, float]
  }

/'
Models
Targets
RMSDs
More metrics: N1, N2, DIST, N, GDT_TS, LGA_S3, LGA_Q


-> List of winner & List of RMSD
'/

Casp *-- Metrics
Casp *-- Group
Group *-- Model
Model *-- Metrics
@enduml
