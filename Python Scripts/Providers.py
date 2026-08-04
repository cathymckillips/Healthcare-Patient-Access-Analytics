exec(r'''
from pathlib import Path
import random
import csv

random.seed(43)

output_folder = Path(r"C:\Users\caths\Desktop\scrip")
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "providers.csv"

number_of_providers = 150

states = [
    "FL", "TX", "CA", "NY", "PA",
    "IL", "OH", "GA", "NC", "MI",
    "NJ", "VA", "WA", "AZ", "MA"
]

provider_specialties = [
    "Rheumatology",
    "Neurology",
    "Dermatology",
    "Gastroenterology"
]

provider_types = [
    "Hospital System",
    "Private Practice",
    "Specialty Clinic"
]

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "ProviderID",
        "ProviderName",
        "ProviderSpecialty",
        "ProviderState",
        "ProviderType"
    ])

    for provider_number in range(1, number_of_providers + 1):
        provider_id = f"PRV{provider_number:05d}"

        provider_name = f"Provider Practice {provider_number:03d}"

        provider_specialty = random.choice(
            provider_specialties
        )

        provider_state = random.choice(states)

        provider_type = random.choices(
            provider_types,
            weights=[35, 40, 25],
            k=1
        )[0]

        writer.writerow([
            provider_id,
            provider_name,
            provider_specialty,
            provider_state,
            provider_type
        ])

print(f"Success! Created {number_of_providers:,} provider records.")
print(f"File saved to: {output_file}")
''')