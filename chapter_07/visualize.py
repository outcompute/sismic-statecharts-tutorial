import os
from sismic.io import import_from_yaml, export_to_plantuml

def generate_diagram():
    # 1. Load the YAML
    filepath = os.path.join(os.path.dirname(__file__), 'vault_complicated.yaml')
    statechart = import_from_yaml(filepath=filepath)

    # 2. Convert to PlantUML text
    # sismic.io.export_to_plantuml returns a string
    puml_code = export_to_plantuml(statechart)
    print(puml_code)

    # 3. Save to file
    print("Diagram source generated. Copy the contents above (from @startuml to @enduml) and paste it into http://www.plantuml.com/plantuml/ to see your chart!")

if __name__ == '__main__':
    generate_diagram()