from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.transaction import Transaction


def classify_transaction(transaction: Transaction) -> dict:
    text = (
        f"{transaction.description} "
        f"{transaction.counterparty}"
    ).lower()

    # Revenue
    if any(keyword in text for keyword in [
        "pos food",
        "pos beverage",
        "catering payment",
        "marketplace payout",
    ]):
        return {
            "category": "Revenue",
            "accounting_treatment": "P&L",
            "confidence": Decimal("0.99"),
            "needs_review": False,
        }

    # Payroll
    if any(keyword in text for keyword in [
        "payroll",
        "salary",
        "wages",
    ]):
        return {
            "category": "Payroll",
            "accounting_treatment": "P&L",
            "confidence": Decimal("0.99"),
            "needs_review": False,
        }

    # Rent
    if "rent" in text:
        return {
            "category": "Rent",
            "accounting_treatment": "P&L",
            "confidence": Decimal("0.99"),
            "needs_review": False,
        }

    # Utilities
    if any(keyword in text for keyword in [
        "electricity",
        "utility",
        "water",
        "gas",
    ]):
        return {
            "category": "Utilities",
            "accounting_treatment": "P&L",
            "confidence": Decimal("0.98"),
            "needs_review": False,
        }

    # Food inventory
    if any(keyword in text for keyword in [
        "food",
        "produce",
        "meat",
        "grocery",
        "food inventory",
    ]):
        return {
            "category": "Food",
            "accounting_treatment": "P&L",
            "confidence": Decimal("0.90"),
            "needs_review": False,
        }

    # Beverage inventory
    if any(keyword in text for keyword in [
        "beverage",
        "beer",
        "wine",
        "liquor",
        "drinks",
    ]):
        return {
            "category": "Beverage",
            "accounting_treatment": "P&L",
            "confidence": Decimal("0.90"),
            "needs_review": False,
        }

    # Marketing
    if any(keyword in text for keyword in [
        "marketing",
        "advertising",
        "ads",
    ]):
        return {
            "category": "Marketing",
            "accounting_treatment": "P&L",
            "confidence": Decimal("0.97"),
            "needs_review": False,
        }

    # Insurance
    if "insurance" in text:
        return {
            "category": "Insurance",
            "accounting_treatment": "P&L",
            "confidence": Decimal("0.98"),
            "needs_review": False,
        }

    # Cleaning
    if any(keyword in text for keyword in [
        "cleaning",
        "janitorial",
    ]):
        return {
            "category": "Cleaning",
            "accounting_treatment": "P&L",
            "confidence": Decimal("0.97"),
            "needs_review": False,
        }

    # Equipment / capital expenditure
    if any(keyword in text for keyword in [
        "equipment",
        "oven",
        "refrigerator",
        "freezer",
        "machine",
    ]):
        return {
            "category": "Equipment",
            "accounting_treatment": "Balance Sheet",
            "confidence": Decimal("0.95"),
            "needs_review": False,
        }

    # Loan principal
    if any(keyword in text for keyword in [
        "loan principal",
        "loan repayment",
        "principal repayment",
    ]):
        return {
            "category": "Loan Repayment",
            "accounting_treatment": "Balance Sheet",
            "confidence": Decimal("0.98"),
            "needs_review": False,
        }

    # Owner distribution
    if any(keyword in text for keyword in [
        "owner distribution",
        "owner withdrawal",
        "owner draw",
    ]):
        return {
            "category": "Owner Distribution",
            "accounting_treatment": "Equity",
            "confidence": Decimal("0.98"),
            "needs_review": False,
        }

    # Sales tax
    if any(keyword in text for keyword in [
        "sales tax",
        "tax remittance",
    ]):
        return {
            "category": "Sales Tax",
            "accounting_treatment": "Balance Sheet",
            "confidence": Decimal("0.98"),
            "needs_review": False,
        }

    # Refund / discount
    if any(keyword in text for keyword in [
        "refund",
        "discount",
    ]):
        return {
            "category": "Refunds & Discounts",
            "accounting_treatment": "P&L",
            "confidence": Decimal("0.95"),
            "needs_review": False,
        }

    # Delivery commission
    if any(keyword in text for keyword in [
        "delivery commission",
        "platform commission",
        "commission",
    ]):
        return {
            "category": "Delivery Commission",
            "accounting_treatment": "P&L",
            "confidence": Decimal("0.95"),
            "needs_review": False,
        }

    # Unknown transaction
    return {
        "category": "Uncategorized",
        "accounting_treatment": "Review Required",
        "confidence": Decimal("0.40"),
        "needs_review": True,
    }


def classify_transactions(db: Session) -> tuple[int, int]:
    transactions = db.query(Transaction).all()

    review_count = 0

    for transaction in transactions:
        result = classify_transaction(transaction)

        transaction.category = result["category"]
        transaction.accounting_treatment = result["accounting_treatment"]
        transaction.confidence = result["confidence"]
        transaction.needs_review = result["needs_review"]

        if result["needs_review"]:
            review_count += 1

    db.commit()

    return len(transactions), review_count