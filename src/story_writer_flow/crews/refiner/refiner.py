from pathlib import Path

from crewai.project import load_crew


def kickoff_refiner_crew(inputs: dict):
    crew, default_inputs = load_crew(Path(__file__).with_name("refiner_crew.jsonc"))
    return crew.kickoff(inputs={**default_inputs, **inputs})