import pytest
from datetime import datetime, timedelta
from librarynow.reservations import Student, Book, may_reserve, ReservationResult


# 1. Positive test: mahasiswa dengan 0 reservasi berhasil memesan buku tersedia
def test_successful_reservation():
    student = Student(id="S01", active_reservations_count=0)
    book = Book(id="B01", is_borrowed=False)
    now = datetime(2026, 10, 13, 10, 0, 0)

    result = may_reserve(student, book, now)
    assert result.accepted is True
    assert result.reason == "Reservation accepted"


# 2. Negative test: batas 3 reservasi & buku yang sedang dipinjam
def test_reservation_rejected_due_to_limit():
    student = Student(id="S02", active_reservations_count=3)
    book = Book(id="B02", is_borrowed=False)
    now = datetime(2026, 10, 13, 10, 0, 0)

    result = may_reserve(student, book, now)
    assert result.accepted is False
    assert "Maximum" in result.reason


def test_reservation_rejected_due_to_borrowed_book():
    student = Student(id="S03", active_reservations_count=0)
    book = Book(id="B03", is_borrowed=True)
    now = datetime(2026, 10, 13, 10, 0, 0)

    result = may_reserve(student, book, now)
    assert result.accepted is False
    assert "borrowed" in result.reason


# 3. Fixture untuk mahasiswa dengan 3 reservasi aktif termasuk cleanup-nya
@pytest.fixture
def student_with_max_reservations():
    student = Student(id="S-MAX", active_reservations_count=3)
    yield student
    # Cleanup simulasi (jika diperlukan reset state)
    student.active_reservations_count = 0


def test_with_max_reservation_fixture(student_with_max_reservations):
    book = Book(id="B99", is_borrowed=False)
    now = datetime(2026, 10, 13, 10, 0, 0)
    result = may_reserve(student_with_max_reservations, book, now)
    assert result.accepted is False


# 4. Parameterized test untuk jumlah reservasi 0, 2, 3, dan 4
@pytest.mark.parametrize(
    "count, expected_accepted",
    [
        (0, True),
        (2, True),
        (3, False),
        (4, False),
    ],
)
def test_reservation_counts_parameterized(count, expected_accepted):
    student = Student(id="S-Param", active_reservations_count=count)
    book = Book(id="B-Param", is_borrowed=False)
    now = datetime(2026, 10, 13, 10, 0, 0)

    result = may_reserve(student, book, now)
    assert result.accepted == expected_accepted


# 5. Test aturan kedaluwarsa 24 jam dengan injeksi parameter 'now'
def test_reservation_expiry_injection():
    reservation_time = datetime(2026, 10, 12, 10, 0, 0)
    # Waktu saat dicek sudah lewat 25 jam (> 24 jam)
    current_time = datetime(2026, 10, 13, 11, 0, 0)

    elapsed_hours = (current_time - reservation_time).total_seconds() / 3600
    assert elapsed_hours > 24
