from exreview.infrastructure.security.argon2_password_hasher import (
    Argon2PasswordHasher,
)


def test_hash_password():
    hasher = Argon2PasswordHasher()

    password = "ExReview-Secure-Password123"
    hashed_password = hasher.hash(password)

    assert hashed_password != password
    assert hashed_password.startswith("$argon2id$")


def test_verify_correct_password():
    hasher = Argon2PasswordHasher()

    password = "ExReview-Secure-Password123"
    hashed_password = hasher.hash(password)

    assert hasher.verify(password, hashed_password) is True


def test_verify_incorrect_password():
    hasher = Argon2PasswordHasher()

    hashed_password = hasher.hash("ExReview-Secure-Password123")

    assert hasher.verify(
        "Wrong-Password123",
        hashed_password
    ) is False


def test_same_password_produces_different_hashes():
    hasher = Argon2PasswordHasher()

    password = "ExReview-Secure-Password123"

    first_hash = hasher.hash(password)
    second_hash = hasher.hash(password)

    assert first_hash != second_hash