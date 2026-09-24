from sqlalchemy.orm import Session

from app.models.transaction import Transaction


def classify_transaction(transaction: Transaction):
    text = (
        f"{transaction.description} "
        f"{transaction.counterparty}"
    ).lower()

    # -------------------------
    # REVENUE
    # -------------------------
    if any(x in text for x in [
        "pos food",
        "food sales",
    ]):
        return "Revenue", 0.98, False, "P&L"

    if any(x in text for x in [
        "pos beverage",
        "beverage sales",
    ]):
        return "Revenue", 0.98, False, "P&L"

    if any(x in text for x in [
        "catering payment",
        "catering invoice payment",
    ]):
        return "Revenue", 0.95, False, "P&L"

    if "marketplace payout" in text:
        return "Revenue", 0.95, False, "P&L"

    # Gift cards are normally a liability until redeemed
    if "gift card" in text:
        return "Gift Card Liability", 0.95, False, "Balance Sheet"

    # -------------------------
    # PAYROLL
    # -------------------------
    if any(x in text for x in [
        "payroll",
        "salary",
        "wages",
    ]):
        return "Payroll", 0.98, False, "P&L"

    # -------------------------
    # RENT
    # -------------------------
    if "rent" in text:
        return "Rent", 0.98, False, "P&L"

    # -------------------------
    # UTILITIES
    # -------------------------
    if any(x in text for x in [
        "electricity",
        "utility",
        "water",
        "gas bill",
        "internet",
        "phone",
    ]):
        return "Utilities", 0.95, False, "P&L"

    # -------------------------
    # FOOD / BEVERAGE
    # -------------------------
    if any(x in text for x in [
        "food inventory",
        "food",
        "produce",
        "meat",
        "grocery",
    ]):
        return "Food", 0.95, False, "P&L"

    if any(x in text for x in [
        "beverage inventory",
        "beverage",
        "beer",
        "wine",
        "liquor",
        "drinks",
    ]):
        return "Beverage", 0.95, False, "P&L"

    # -------------------------
    # MARKETING
    # -------------------------
    if any(x in text for x in [
        "marketing",
        "advertising",
        "advertisement",
        "ads",
    ]):
        return "Marketing", 0.95, False, "P&L"

    # -------------------------
    # INSURANCE
    # -------------------------
    if "insurance" in text:
        return "Insurance", 0.98, False, "P&L"

    # -------------------------
    # CLEANING
    # -------------------------
    if any(x in text for x in [
        "cleaning",
        "janitorial",
    ]):
        return "Cleaning", 0.95, False, "P&L"

    # -------------------------
    # DELIVERY COMMISSION
    # -------------------------
    if any(x in text for x in [
        "delivery commission",
        "platform commission",
        "commission",
    ]):
        return "Delivery Commission", 0.95, False, "P&L"

    # -------------------------
    # REFUNDS / DISCOUNTS
    # -------------------------
    if any(x in text for x in [
        "refund",
        "discount",
    ]):
        return "Refunds & Discounts", 0.95, False, "P&L"

    # -------------------------
    # OFFICE / ADMIN
    # -------------------------
    # These are plausible classifications,
    # but still need human review.
    if any(x in text for x in [
        "office supplies",
        "office/admin",
        "admin supplies",
        "stationery",
    ]):
        return "Office/Admin Supplies", 0.75, True, "P&L"

    # -------------------------
    # REPAIRS
    # -------------------------
    if any(x in text for x in [
        "repair",
        "maintenance",
    ]):
        return "Repairs & Maintenance", 0.75, True, "P&L"

    # -------------------------
    # SOFTWARE / LICENSE
    # -------------------------
    if any(x in text for x in [
        "pos/software",
        "software subscription",
        "pos subscription",
        "software",
    ]):
        return "POS/Software Subscription", 0.75, True, "P&L"

    if any(x in text for x in [
        "annual license",
        "license renewal",
    ]):
        return "POS/Software Subscription", 0.70, True, "P&L"

    # -------------------------
    # ACCOUNTING
    # -------------------------
    if any(x in text for x in [
        "accounting",
        "bookkeeping",
    ]):
        return "Accounting/Bookkeeping", 0.80, True, "P&L"

    # -------------------------
    # PACKAGING
    # -------------------------
    if any(x in text for x in [
        "packaging",
        "disposables",
        "to-go",
    ]):
        return "To-go Packaging & Disposables", 0.75, True, "P&L"

    # -------------------------
    # EQUIPMENT
    # -------------------------
    if any(x in text for x in [
        "equipment",
        "oven",
        "refrigerator",
        "freezer",
        "machine",
    ]):
        return "Equipment", 0.98, False, "Balance Sheet"

    # -------------------------
    # LOAN PRINCIPAL
    # -------------------------
    if any(x in text for x in [
        "loan principal",
        "loan repayment",
        "principal repayment",
    ]):
        return "Loan Repayment", 0.98, False, "Balance Sheet"

    # -------------------------
    # OWNER DISTRIBUTION
    # -------------------------
    if any(x in text for x in [
        "owner distribution",
        "owner withdrawal",
        "owner draw",
    ]):
        return "Owner Distribution", 0.98, False, "Equity"

    # -------------------------
    # SALES TAX
    # -------------------------
    if any(x in text for x in [
        "sales tax",
        "tax remittance",
    ]):
        return "Sales Tax", 0.98, False, "Balance Sheet"

    # -------------------------
    # UNKNOWN / REVIEW
    # -------------------------
    return "Uncategorized", 0.40, True, None


def classify_transactions(db: Session):
    transactions = db.query(Transaction).all()

    review_count = 0

    for transaction in transactions:
        (
            category,
            confidence,
            needs_review,
            accounting_treatment,
        ) = classify_transaction(transaction)

        transaction.category = category
        transaction.confidence = confidence
        transaction.needs_review = needs_review
        transaction.accounting_treatment = accounting_treatment

        if needs_review:
            review_count += 1

    db.commit()

    return len(transactions), review_count