import string

def get_common_passwords_set():
    try:
        with open("common_passwords.txt", "r") as f:
            return set(line.strip().lower() for line in f)
    except:
        return set(["password", "123456", "qwerty", "letmein", "welcome"])

def check_password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters.")

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

    if password.lower() in get_common_passwords_set():
        feedback.append("Password is a common password!")
        score = 0

    strength = {0: "Very Weak", 1: "Weak", 2: "Medium", 3: "Strong", 4: "Very Strong", 5: "Excellent"}
    return strength.get(score, "Unknown"), feedback

if __name__ == "__main__":
    password = input("Enter a password to check strength: ")
    strength, feedback = check_password_strength(password)
    print(f"Strength: {strength}")
    if feedback:
        print("Feedback:")
        for line in feedback:
            print("-", line)