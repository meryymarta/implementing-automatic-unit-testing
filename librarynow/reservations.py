from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class ReservationResult:
    accepted: bool
    reason: str = ""


@dataclass
class Student:
    id: str
    active_reservations_count: int = 0
    has_borrowed_book: bool = False


@dataclass
class Book:
    id: str
    is_borrowed: bool = False


def may_reserve(student: Student, book: Book, now: datetime) -> ReservationResult:
    # Aturan 1: Buku yang sedang dipinjam tidak dapat dipesan
    if book.is_borrowed:
        return ReservationResult(accepted=False, reason="Book is currently borrowed")

    # Aturan 2: Batas maksimal 3 reservasi aktif
    if student.active_reservations_count >= 3:
        return ReservationResult(
            accepted=False, reason="Maximum active reservations reached"
        )

    return ReservationResult(accepted=True, reason="Reservation accepted")
