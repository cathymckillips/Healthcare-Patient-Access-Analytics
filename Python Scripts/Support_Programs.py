exec(r'''
from pathlib import Path
import csv
import random
from datetime import datetime, timedelta

random.seed(47)

output_folder = Path(r"C:\Users\caths\Desktop\scrip")

patients_file = output_folder / "patients.csv"
claims_file = output_folder / "claims.csv"

output_file = output_folder / "support_programs.csv"

# --------------------------------------------------
# Read Patients
# --------------------------------------------------

patients = []

with open(patients_file,newline="",encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:
        patients.append(row)

# --------------------------------------------------
# Read Claims
# --------------------------------------------------

claim_lookup = {}

with open(claims_file,newline="",encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        claim_lookup[row["PatientID"]] = row

# --------------------------------------------------
# Create Support Program File
# --------------------------------------------------

with open(output_file,"w",newline="",encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([

        "SupportID",
        "PatientID",
        "FinancialAssistance",
        "NurseSupport",
        "CaseManager",
        "EducationProgram",
        "EnrollmentDate",
        "ProgramStatus"

    ])

    support_number = 1

    financial_count = 0
    nurse_count = 0
    case_count = 0
    education_count = 0

    for patient in patients:

        patient_id = patient["PatientID"]

        enrollment_date = datetime.strptime(
            patient["EnrollmentDate"],
            "%Y-%m-%d"
        )

        claim = claim_lookup.get(patient_id)

        financial = "No"

        if claim:

            oop = float(claim["PatientResponsibility"])

            if oop > 300:

                financial = random.choices(
                    ["Yes","No"],
                    weights=[75,25],
                    k=1
                )[0]

            else:

                financial = random.choices(
                    ["Yes","No"],
                    weights=[20,80],
                    k=1
                )[0]

        nurse = random.choices(
            ["Yes","No"],
            weights=[35,65],
            k=1
        )[0]

        case_manager = random.choices(
            ["Yes","No"],
            weights=[45,55],
            k=1
        )[0]

        education = random.choices(
            ["Yes","No"],
            weights=[55,45],
            k=1
        )[0]

        if financial=="Yes":
            financial_count+=1

        if nurse=="Yes":
            nurse_count+=1

        if case_manager=="Yes":
            case_count+=1

        if education=="Yes":
            education_count+=1

        support_date = enrollment_date + timedelta(
            days=random.randint(0,5)
        )

        status = random.choices(
            ["Active","Completed"],
            weights=[82,18],
            k=1
        )[0]

        writer.writerow([

            f"SUP{support_number:07d}",
            patient_id,
            financial,
            nurse,
            case_manager,
            education,
            support_date.date(),
            status

        ])

        support_number += 1

print()

print("Support Program records created.")

print(f"Total Patients: {support_number-1:,}")

print(f"Financial Assistance: {financial_count:,}")

print(f"Nurse Support: {nurse_count:,}")

print(f"Case Managers: {case_count:,}")

print(f"Education Programs: {education_count:,}")

print(output_file)

''')