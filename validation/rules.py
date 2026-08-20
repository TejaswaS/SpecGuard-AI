from dataclasses import dataclass

@dataclass
class ValidationIssue:
    field : str
    severity : str
    message : str
    recommendation : str

def validate_product(product):
    issues = []

    specifications = {
        spec.name.lower(): spec for spec in product.specifications
    }
    ## Rule-1 : Missing important fields
    important_fields = [
        "power"
        "voltage"
        "pressure"
    ]
    for field in important_fields:
        if field not in specifications:
            issues.append(
                ValidationIssue(
                    field=field,
                    severity="MISSING",
                    message=f"{field.title()} specification is missing.",
                    recommendation=f"Add verified {field} information."   
                )
            ) 

     # --------------------------------
    # Rule 2: Negative numeric values
    # --------------------------------

    for spec in product.specifications:

        if not spec.value:
            continue

        try:
            numeric_value = float(
                spec.value.replace(",", "").split()[0]
            )

            if numeric_value < 0:

                issues.append(
                    ValidationIssue(
                        field=spec.name,
                        severity="ERROR",
                        message=f"{spec.name} has a negative value: {spec.value}",
                        recommendation="Verify the value in the original datasheet."
                    )
                )

        except (ValueError, IndexError):
            pass

    # --------------------------------
    # Rule 3: Suspicious pressure
    # --------------------------------

    pressure = specifications.get("pressure")

    if pressure and pressure.value:

        try:

            value = float(
                pressure.value.replace(",", "").split()[0]
            )

            unit = (pressure.unit or "").lower()

            if unit == "bar" and value > 1000:

                issues.append(
                    ValidationIssue(
                        field="Pressure",
                        severity="ERROR",
                        message=f"Pressure value {value} bar looks unusually high.",
                        recommendation="Verify the pressure value and unit."
                    )
                )

        except (ValueError, IndexError):
            pass

    # --------------------------------
    # Rule 4: Missing source evidence
    # --------------------------------

    for spec in product.specifications:

        if not spec.source_text:

            issues.append(
                ValidationIssue(
                    field=spec.name,
                    severity="WARNING",
                    message="No source evidence was captured.",
                    recommendation="Review the original document."
                )
            )

    return issues          