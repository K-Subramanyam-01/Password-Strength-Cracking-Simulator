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
    try:
        bf_max_attempts = int(input("Enter brute-force max attempts (>= 2000000 for length 4): "))
    except:
        bf_max_attempts = 2000000
    brute_force_attack(hash_val, length=bf_length, algo=algo, max_attempts=bf_max_attempts)