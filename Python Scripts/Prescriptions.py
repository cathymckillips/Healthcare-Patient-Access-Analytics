exec(r'''
from pathlib import Path
import random
import csv
from datetime import datetime, timedelta

random.seed(44)

output_folder = Path(r"C:\Users\caths\Desktop\scrip")

patients_file = output_folder / "patients.csv"
providers_file = output_folder / "providers.csv"
output_file = output_folder / "prescriptions.csv"

# -------------------------------
# Read Patients
# -------------------------------

patients = []

with open(patients_file, newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        patients.append(row)

# -------------------------------
# Read Providers
# -------------------------------

providers = []

with open(providers_file, newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        providers.append(row)

# -------------------------------
# Medication Master
# -------------------------------

medications = [

    ("Therava","Rheumatoid Arthritis"),
    ("Neurovia","Multiple Sclerosis"),
    ("Dermexa","Psoriasis"),
    ("Crohnixa","Crohn's Disease")

]

channels = [
    "Physician Office",
    "Hospital",
    "Telehealth"
]

# -------------------------------
# Create Prescription File
# -------------------------------

with open(output_file,"w",newline="",encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([
        "PrescriptionID",
        "PatientID",
        "ProviderID",
        "Medication",
        "Diagnosis",
        "PrescriptionDate",
        "Quantity",
        "DaysSupply",
        "OrderChannel"
    ])

    prescription_number = 1

    for patient in patients:

        patient_id = patient["PatientID"]

        provider = random.choice(providers)

        provider_id = provider["ProviderID"]

        diagnosis = patient["Diagnosis"]

        medication = next(
            med for med,diag in medications
            if diag == diagnosis
        )

        enrollment_date = datetime.strptime(
            patient["EnrollmentDate"],
            "%Y-%m-%d"
        )

        prescription_date = enrollment_date + timedelta(
            days=random.randint(0,15)
        )

        quantity = random.choice([
            1,
            1,
            1,
            2,
            3
        ])

        days_supply = random.choice([
            28,
            30,
            60,
            90
        ])

        order_channel = random.choice(channels)

        writer.writerow([

            f"RX{prescription_number:07d}",
            patient_id,
            provider_id,
            medication,
            diagnosis,
            prescription_date.date(),
            quantity,
            days_supply,
            order_channel

        ])

        prescription_number += 1

print()

print("Prescription records created.")

print(f"Total Prescriptions: {prescription_number-1:,}")

print(output_file)

''')