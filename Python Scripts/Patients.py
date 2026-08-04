exec(r'''
from pathlib import Path
import random
import csv
from datetime import date, timedelta

random.seed(42)

output_folder = Path(r"C:\Users\caths\Desktop\scrip")
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "patients.csv"

number_of_patients = 10000

states = [
    "FL", "TX", "CA", "NY", "PA",
    "IL", "OH", "GA", "NC", "MI",
    "NJ", "VA", "WA", "AZ", "MA"
]

diagnoses = [
    "Rheumatoid Arthritis",
    "Multiple Sclerosis",
    "Psoriasis",
    "Crohn's Disease"
]

insurance_plans = [
    "Apex Commercial",
    "Unity Health",
    "PrimeCare",
    "National Choice",
    "Federal Health",
    "Community Medicaid",
    "Senior Medicare"
]

payer_types = {
    "Apex Commercial": "Commercial",
    "Unity Health": "Commercial",
    "PrimeCare": "Commercial",
    "National Choice": "Commercial",
    "Federal Health": "Government",
    "Community Medicaid": "Medicaid",
    "Senior Medicare": "Medicare"
}

genders = [
    "Female",
    "Male",
    "Nonbinary",
    "Not Reported"
]

start_date = date(2025, 1, 1)
end_date = date(2026, 6, 30)
date_range_days = (end_date - start_date).days

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "PatientID",
        "BirthYear",
        "AgeAtEnrollment",
        "Gender",
        "State",
        "Diagnosis",
        "InsurancePlan",
        "PayerType",
        "EnrollmentDate"
    ])

    for patient_number in range(1, number_of_patients + 1):
        patient_id = f"PAT{patient_number:07d}"

        birth_year = random.randint(1945, 2004)

        enrollment_date = start_date + timedelta(
            days=random.randint(0, date_range_days)
        )

        age_at_enrollment = enrollment_date.year - birth_year

        gender = random.choices(
            genders,
            weights=[50, 46, 1, 3],
            k=1
        )[0]

        state = random.choice(states)
        diagnosis = random.choice(diagnoses)

        insurance_plan = random.choices(
            insurance_plans,
            weights=[18, 15, 14, 16, 10, 12, 15],
            k=1
        )[0]

        payer_type = payer_types[insurance_plan]

        writer.writerow([
            patient_id,
            birth_year,
            age_at_enrollment,
            gender,
            state,
            diagnosis,
            insurance_plan,
            payer_type,
            enrollment_date.isoformat()
        ])

print(f"Success! Created {number_of_patients:,} patient records.")
print(f"File saved to: {output_file}")
''')