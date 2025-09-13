import string
import itertools
import hashlib
import time

# --------- Password Strength Checker ---------

def check_password_strength(password):
    score = 0
    feedback = []

    # Length check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters.")

    # Uppercase, lowercase, digits, symbols
    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Add digits.")
    if any(c in string.punctuation for c in password):
        score += 1
    else:
        feedback.append("Add symbols.")

    # Common patterns
    if password.lower() in get_common_passwords_set():
        feedback.append("Password is a common password!")
        score = 0

    # Scoring
    strength = {0: "Very Weak", 1: "Weak", 2: "Medium", 3: "Strong", 4: "Very Strong", 5: "Excellent"}
    return strength.get(score, "Unknown"), feedback

def get_common_passwords_set():
    # Load a list of common passwords; this can be replaced with a larger list (e.g., rockyou.txt)
    try:
        with open("common_passwords.txt", "r") as f:
            return set(line.strip().lower() for line in f)
    except:
        return set(["password", "123456", "qwerty", "letmein", "welcome"])

# --------- Password Cracking Simulation ---------

def hash_password(password, algo="sha256"):
    if algo == "sha256":
        return hashlib.sha256(password.encode()).hexdigest()
    elif algo == "md5":
        return hashlib.md5(password.encode()).hexdigest()

def dictionary_attack(hash_to_crack, algo="sha256"):
    print("Starting dictionary attack...")
    for pwd in get_common_passwords_set():
        if hash_password(pwd, algo) == hash_to_crack:
            print(f"Password found (dictionary): {pwd}")
            return pwd
    print("Dictionary attack failed.")
    return None

def brute_force_attack(hash_to_crack, length=4, charset=None, algo="sha256", max_attempts=100000):
    print("Starting brute-force attack...")
    if charset is None:
        charset = string.ascii_lowercase + string.digits
    attempts = 0
    start = time.time()
    for pwd_tuple in itertools.product(charset, repeat=length):
        pwd = ''.join(pwd_tuple)
        attempts += 1
        if hash_password(pwd, algo) == hash_to_crack:
            end = time.time()
            print(f"Password found (brute-force): {pwd} in {attempts} attempts, {end-start:.2f}s")
            return pwd
        if attempts >= max_attempts:
            print("Brute-force attack aborted (max attempts reached).")
            break
    print("Brute-force attack failed.")
    return None

# --------- Demo Section ---------
if __name__ == "__main__":
    print("=== Password Strength Checker ===")
    password = input("Enter a password to check strength: ")
    strength, feedback = check_password_strength(password)
    print(f"Strength: {strength}")
    if feedback:
        print("Feedback:")
        for line in feedback:
            print("-", line)

    print("\n=== Password Cracking Simulation ===")
    # Simulate password hashing
    password_to_crack = input("Enter a password to hash and crack: ")
    algo = "sha256"
    hash_val = hash_password(password_to_crack, algo)
    print(f"Hashed password ({algo}): {hash_val}")

    # Dictionary attack
    dictionary_attack(hash_val, algo)

    # Brute-force attack (demo: length up to 4, for speed)
    try:
        bf_length = int(input("Enter brute-force max length (recommended <= 4): "))
    except:
        bf_length = 4
    brute_force_attack(hash_val, length=bf_length, algo=algo)