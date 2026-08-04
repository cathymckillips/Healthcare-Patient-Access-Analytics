exec(r'''
from pathlib import Path
import csv
import random
from datetime import datetime, timedelta

random.seed(48)

output_folder = Path(r"C:\Users\caths\Desktop\scrip")

claims_file = output_folder / "claims.csv"
prescriptions_file = output_folder / "prescriptions.csv"
output_file = output_folder / "pharmacy_fulfillment.csv"

# ---------------------------------------------------------
# Read prescriptions
# ---------------------------------------------------------

prescription_lookup = {}

with open(
    prescriptions_file,
    newline="",
    encoding="utf-8"
) as file:
    reader = csv.DictReader(file)

    for row in reader:
        prescription_lookup[row["PrescriptionID"]] = row

# ---------------------------------------------------------
# Read claims
# ---------------------------------------------------------

claims = []

with open(
    claims_file,
    newline="",
    encoding="utf-8"
) as file:
    reader = csv.DictReader(file)

    for row in reader:
        claims.append(row)

# ---------------------------------------------------------
# Pharmacy reference data
# ---------------------------------------------------------

pharmacy_names = {
    "PHM001": "NorthStar Specialty Pharmacy",
    "PHM002": "Summit Specialty Pharmacy",
    "PHM003": "CareBridge Specialty Pharmacy",
    "PHM004": "Horizon Specialty Pharmacy"
}

pharmacy_fill_ranges = {
    "PHM001": (1, 3),
    "PHM002": (2, 5),
    "PHM003": (1, 4),
    "PHM004": (3, 8)
}

shipping_methods = [
    "Standard",
    "Expedited",
    "Overnight"
]

delivery_statuses = [
    "Delivered",
    "Delayed",
    "Returned"
]

# ---------------------------------------------------------
# Create pharmacy fulfillment records
# ---------------------------------------------------------

fulfillment_count = 0
delivered_count = 0
delayed_count = 0
returned_count = 0

with open(
    output_file,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "FulfillmentID",
        "ClaimID",
        "PrescriptionID",
        "PatientID",
        "PharmacyID",
        "PharmacyName",
        "Medication",
        "ClaimDecisionDate",
        "FillDate",
        "ShipmentDate",
        "DeliveryDate",
        "ShippingMethod",
        "DeliveryStatus",
        "FillDays",
        "ShippingDays",
        "TotalFulfillmentDays",
        "PrescriptionToDeliveryDays"
    ])

    for claim in claims:

        if claim["ClaimStatus"] != "Paid":
            continue

        claim_id = claim["ClaimID"]
        prescription_id = claim["PrescriptionID"]
        patient_id = claim["PatientID"]
        pharmacy_id = claim["PharmacyID"]

        prescription = prescription_lookup[prescription_id]

        medication = prescription["Medication"]

        prescription_date = datetime.strptime(
            prescription["PrescriptionDate"],
            "%Y-%m-%d"
        )

        claim_decision_date = datetime.strptime(
            claim["ClaimDecisionDate"],
            "%Y-%m-%d"
        )

        minimum_fill_days, maximum_fill_days = (
            pharmacy_fill_ranges[pharmacy_id]
        )

        fill_days = random.randint(
            minimum_fill_days,
            maximum_fill_days
        )

        fill_date = (
            claim_decision_date
            + timedelta(days=fill_days)
        )

        shipping_method = random.choices(
            shipping_methods,
            weights=[55, 30, 15],
            k=1
        )[0]

        if shipping_method == "Standard":
            shipping_days = random.randint(3, 6)

        elif shipping_method == "Expedited":
            shipping_days = random.randint(2, 3)

        else:
            shipping_days = 1

        shipment_date = (
            fill_date
            + timedelta(days=random.randint(0, 2))
        )

        delivery_status = random.choices(
            delivery_statuses,
            weights=[92, 6, 2],
            k=1
        )[0]

        if delivery_status == "Delayed":
            shipping_days += random.randint(2, 5)
            delayed_count += 1

        elif delivery_status == "Returned":
            shipping_days += random.randint(2, 4)
            returned_count += 1

        else:
            delivered_count += 1

        delivery_date = (
            shipment_date
            + timedelta(days=shipping_days)
        )

        total_fulfillment_days = (
            delivery_date - claim_decision_date
        ).days

        prescription_to_delivery_days = (
            delivery_date - prescription_date
        ).days

        fulfillment_count += 1

        writer.writerow([
            f"FUL{fulfillment_count:07d}",
            claim_id,
            prescription_id,
            patient_id,
            pharmacy_id,
            pharmacy_names[pharmacy_id],
            medication,
            claim_decision_date.date().isoformat(),
            fill_date.date().isoformat(),
            shipment_date.date().isoformat(),
            delivery_date.date().isoformat(),
            shipping_method,
            delivery_status,
            fill_days,
            shipping_days,
            total_fulfillment_days,
            prescription_to_delivery_days
        ])

print("Success! Pharmacy fulfillment records created.")
print(f"Total fulfillment records: {fulfillment_count:,}")
print(f"Delivered: {delivered_count:,}")
print(f"Delayed: {delayed_count:,}")
print(f"Returned: {returned_count:,}")
print(f"File saved to: {output_file}")
''')