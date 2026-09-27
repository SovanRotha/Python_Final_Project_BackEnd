from sqlalchemy.orm import Session

from app.models.budget.budget import Budget


def list_user_budgets(db: Session, user_id: int) -> list[Budget]:
    return db.query(Budget).filter(Budget.user_id == user_id).all()
