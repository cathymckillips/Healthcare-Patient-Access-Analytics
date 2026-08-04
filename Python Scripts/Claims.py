exec(r'''
from pathlib import Path
import random
import csv
from datetime import datetime, timedelta

random.seed(46)

output_folder = Path(r"C:\Users\caths\Desktop\scrip")

patients_file = output_folder / "patients.csv"
prescriptions_file = output_folder / "prescriptions.csv"
prior_authorizations_file = output_folder / "prior_authorizations.csv"
output_file = output_folder / "claims.csv"

# ---------------------------------------------------------
# Read patient insurance information
# ---------------------------------------------------------

patient_lookup = {}

with open(patients_file, newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        patient_lookup[row["PatientID"]] = {
            "InsurancePlan": row["InsurancePlan"],
            "PayerType": row["PayerType"]
        }

# ---------------------------------------------------------
# Read prescriptions
# ---------------------------------------------------------

prescriptions = {}

with open(prescriptions_file, newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        prescriptions[row["PrescriptionID"]] = row

# ---------------------------------------------------------
# Read prior authorizations
# ---------------------------------------------------------

prior_authorizations = []

with open(
    prior_authorizations_file,
    newline="",
    encoding="utf-8"
) as file:
    reader = csv.DictReader(file)

    for row in reader:
        prior_authorizations.append(row)

# ---------------------------------------------------------
# Business rules
# ---------------------------------------------------------

claim_paid_probability = {
    "Approved": 0.92,
    "Approved After Appeal": 0.86,
    "Denied": 0.08
}

payer_allowed_percentages = {
    "Commercial": (0.72, 0.88),
    "Government": (0.78, 0.92),
    "Medicaid": (0.82, 0.96),
    "Medicare": (0.76, 0.91)
}

patient_responsibility_ranges = {
    "Commercial": (75, 850),
    "Government": (25, 300),
    "Medicaid": (0, 75),
    "Medicare": (40, 450)
}

rejection_reasons = [
    "Authorization Not Found",
    "Coverage Inactive",
    "Duplicate Claim",
    "Invalid Procedure Code",
    "Timely Filing Limit Exceeded",
    "Non-Covered Service"
]

rejection_reason_weights = [
    28,
    18,
    14,
    12,
    10,
    18
]

pharmacy_ids = [
    "PHM001",
    "PHM002",
    "PHM003",
    "PHM004"
]

# ---------------------------------------------------------
# Create claim records
# ---------------------------------------------------------

paid_count = 0
rejected_count = 0
pending_count = 0

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "ClaimID",
        "PrescriptionID",
        "PriorAuthorizationID",
        "PatientID",
        "InsurancePlan",
        "PayerType",
        "PharmacyID",
        "ClaimSubmissionDate",
        "ClaimDecisionDate",
        "ClaimStatus",
        "RejectionReason",
        "BilledAmount",
        "AllowedAmount",
        "PlanPaidAmount",
        "PatientResponsibility"
    ])

    for claim_number, authorization in enumerate(
        prior_authorizations,
        start=1
    ):
        prescription_id = authorization["PrescriptionID"]
        patient_id = authorization["PatientID"]
        prior_authorization_id = authorization[
            "PriorAuthorizationID"
        ]

        prescription = prescriptions[prescription_id]
        patient = patient_lookup[patient_id]

        insurance_plan = patient["InsurancePlan"]
        payer_type = patient["PayerType"]

        final_status = authorization["FinalStatus"]

        if authorization["AppealDecisionDate"]:
            authorization_end_date = datetime.strptime(
                authorization["AppealDecisionDate"],
                "%Y-%m-%d"
            )
        else:
            authorization_end_date = datetime.strptime(
                authorization["PADecisionDate"],
                "%Y-%m-%d"
            )

        claim_submission_date = (
            authorization_end_date
            + timedelta(days=random.randint(1, 7))
        )

        paid_probability = claim_paid_probability[final_status]
        random_value = random.random()

        if random_value < paid_probability:
            claim_status = "Paid"
            rejection_reason = ""
            decision_days = random.randint(1, 8)
            paid_count += 1

        elif random_value < paid_probability + 0.08:
            claim_status = "Pending"
            rejection_reason = ""
            decision_days = random.randint(3, 14)
            pending_count += 1

        else:
            claim_status = "Rejected"
            rejection_reason = random.choices(
                rejection_reasons,
                weights=rejection_reason_weights,
                k=1
            )[0]
            decision_days = random.randint(1, 10)
            rejected_count += 1

        claim_decision_date = (
            claim_submission_date
            + timedelta(days=decision_days)
        )

        billed_amount = round(
            random.uniform(4200, 9800),
            2
        )

        if claim_status == "Paid":
            minimum_allowed, maximum_allowed = (
                payer_allowed_percentages[payer_type]
            )

            allowed_percentage = random.uniform(
                minimum_allowed,
                maximum_allowed
            )

            allowed_amount = round(
                billed_amount * allowed_percentage,
                2
            )

            minimum_patient, maximum_patient = (
                patient_responsibility_ranges[payer_type]
            )

            patient_responsibility = round(
                random.uniform(
                    minimum_patient,
                    maximum_patient
                ),
                2
            )

            patient_responsibility = min(
                patient_responsibility,
                allowed_amount
            )

            plan_paid_amount = round(
                allowed_amount - patient_responsibility,
                2
            )

        else:
            allowed_amount = 0.00
            plan_paid_amount = 0.00
            patient_responsibility = 0.00

        writer.writerow([
            f"CLM{claim_number:07d}",
            prescription_id,
            prior_authorization_id,
            patient_id,
            insurance_plan,
            payer_type,
            random.choice(pharmacy_ids),
            claim_submission_date.date().isoformat(),
            claim_decision_date.date().isoformat(),
            claim_status,
            rejection_reason,
            f"{billed_amount:.2f}",
            f"{allowed_amount:.2f}",
            f"{plan_paid_amount:.2f}",
            f"{patient_responsibility:.2f}"
        ])

print("Success! Claim records created.")
print(f"Total claims: {len(prior_authorizations):,}")
print(f"Paid claims: {paid_count:,}")
print(f"Rejected claims: {rejected_count:,}")
print(f"Pending claims: {pending_count:,}")
print(f"File saved to: {output_file}")
''')