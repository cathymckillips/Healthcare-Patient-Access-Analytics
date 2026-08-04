exec(r'''
from pathlib import Path
import random
import csv
from datetime import datetime, timedelta

random.seed(45)

output_folder = Path(r"C:\Users\caths\Desktop\scrip")

patients_file = output_folder / "patients.csv"
prescriptions_file = output_folder / "prescriptions.csv"
output_file = output_folder / "prior_authorizations.csv"

# ---------------------------------------------------------
# Read patient insurance information
# ---------------------------------------------------------

patient_insurance = {}

with open(patients_file, newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        patient_insurance[row["PatientID"]] = row["InsurancePlan"]

# ---------------------------------------------------------
# Read prescriptions
# ---------------------------------------------------------

prescriptions = []

with open(prescriptions_file, newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        prescriptions.append(row)

# ---------------------------------------------------------
# Business rules
# ---------------------------------------------------------

approval_probabilities = {
    "Apex Commercial": 0.83,
    "Unity Health": 0.78,
    "PrimeCare": 0.75,
    "National Choice": 0.80,
    "Federal Health": 0.86,
    "Community Medicaid": 0.68,
    "Senior Medicare": 0.73
}

denial_reasons = [
    "Missing Clinical Documentation",
    "Step Therapy Required",
    "Non-Formulary Medication",
    "Coverage Terminated",
    "Diagnosis Not Covered",
    "Prior Authorization Expired"
]

denial_reason_weights = [
    26,
    22,
    20,
    8,
    14,
    10
]

# ---------------------------------------------------------
# Create prior authorization records
# ---------------------------------------------------------

approved_count = 0
denied_count = 0
appeal_count = 0
appeal_success_count = 0

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "PriorAuthorizationID",
        "PrescriptionID",
        "PatientID",
        "InsurancePlan",
        "PASubmissionDate",
        "PADecisionDate",
        "DecisionDays",
        "PAStatus",
        "DenialReason",
        "AppealSubmitted",
        "AppealDecisionDate",
        "AppealOutcome",
        "FinalStatus"
    ])

    for authorization_number, prescription in enumerate(
        prescriptions,
        start=1
    ):
        prescription_id = prescription["PrescriptionID"]
        patient_id = prescription["PatientID"]
        insurance_plan = patient_insurance[patient_id]

        prescription_date = datetime.strptime(
            prescription["PrescriptionDate"],
            "%Y-%m-%d"
        )

        submission_delay = random.randint(0, 5)

        pa_submission_date = (
            prescription_date
            + timedelta(days=submission_delay)
        )

        decision_days = random.randint(1, 15)

        pa_decision_date = (
            pa_submission_date
            + timedelta(days=decision_days)
        )

        approval_probability = approval_probabilities[
            insurance_plan
        ]

        approved = random.random() < approval_probability

        if approved:
            pa_status = "Approved"
            denial_reason = ""
            appeal_submitted = "No"
            appeal_decision_date = ""
            appeal_outcome = ""
            final_status = "Approved"
            approved_count += 1

        else:
            pa_status = "Denied"

            denial_reason = random.choices(
                denial_reasons,
                weights=denial_reason_weights,
                k=1
            )[0]

            denied_count += 1

            appeal_submitted_flag = random.random() < 0.55

            if appeal_submitted_flag:
                appeal_submitted = "Yes"
                appeal_count += 1

                appeal_days = random.randint(3, 14)

                appeal_decision_date_value = (
                    pa_decision_date
                    + timedelta(days=appeal_days)
                )

                appeal_decision_date = (
                    appeal_decision_date_value.date().isoformat()
                )

                appeal_success = random.random() < 0.42

                if appeal_success:
                    appeal_outcome = "Approved"
                    final_status = "Approved After Appeal"
                    appeal_success_count += 1
                else:
                    appeal_outcome = "Denied"
                    final_status = "Denied"

            else:
                appeal_submitted = "No"
                appeal_decision_date = ""
                appeal_outcome = ""
                final_status = "Denied"

        writer.writerow([
            f"PA{authorization_number:07d}",
            prescription_id,
            patient_id,
            insurance_plan,
            pa_submission_date.date().isoformat(),
            pa_decision_date.date().isoformat(),
            decision_days,
            pa_status,
            denial_reason,
            appeal_submitted,
            appeal_decision_date,
            appeal_outcome,
            final_status
        ])

print("Success! Prior authorization records created.")
print(f"Total records: {len(prescriptions):,}")
print(f"Initial approvals: {approved_count:,}")
print(f"Initial denials: {denied_count:,}")
print(f"Appeals submitted: {appeal_count:,}")
print(f"Successful appeals: {appeal_success_count:,}")
print(f"File saved to: {output_file}")
''')