from sqlalchemy.orm import Session

from app.models.expense import Expense


def list_user_expenses(db: Session, user_id: int) -> list[Expense]:
    return db.query(Expense).filter(Expense.user_id == user_id).all()