import hashlib
import string
import itertools
import time

def hash_password(password, algo="sha256"):
    if algo == "sha256":
        return hashlib.sha256(password.encode()).hexdigest()
    elif algo == "md5":
        return hashlib.md5(password.encode()).hexdigest()

def get_common_passwords_set():
    try:
        with open("common_passwords.txt", "r") as f:
            return set(line.strip().lower() for line in f if line.strip())
    except FileNotFoundError:
        print("Could not find the file common_passwords.txt.")
        return set()

def dictionary_attack(hash_to_crack, algo="sha256"):
    print("Starting dictionary attack...")
    common_passwords = get_common_passwords_set()
    if not common_passwords:
        print("Dictionary attack failed: No passwords loaded.")
        return None
    for pwd in common_passwords:
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

if __name__ == "__main__":
    password_to_crack = input("Enter a password to hash and crack: ")
    algo = "sha256"
    hash_val = hash_password(password_to_crack, algo)
    print(f"Hashed password ({algo}): {hash_val}")

    dictionary_attack(hash_val, algo)

    try:
        bf_length = int(input("Enter brute-force max length (recommended <= 4): "))
    except:
        bf_length = 4
    brute_force_attack(hash_val, length=bf_length, algo=algo)