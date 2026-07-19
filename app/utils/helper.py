from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def compute_total(quantity: int, unit_amount: float) -> float:
    """Rounds to 2 decimal places to avoid float drift in money fields."""
    return round(quantity * unit_amount, 2)
