import UI

def strength_test():
    UI.header("Password Strength Audit", "Comprehensive complexity evaluation")
    
    password = UI.prompt_secret("Enter password to evaluate")
    if not password:
        UI.warning("Password cannot be empty.")
        return

    score = 0
    suggestions = []

    password_length = len(password)
    has_length = password_length >= 8
    if has_length:
        score += 1
    else:
        suggestions.append("Increase password length to at least 8 characters (14+ recommended).")

    has_upper = any(c.isupper() for c in password)
    if has_upper:
        score += 1
    else:
        suggestions.append("Include uppercase letters (A-Z).")

    has_lower = any(c.islower() for c in password)
    if has_lower:
        score += 1
    else:
        suggestions.append("Include lowercase letters (a-z).")

    has_digit = any(c.isdigit() for c in password)
    if has_digit:
        score += 1
    else:
        suggestions.append("Include numerical digits (0-9).")

    special_characters = "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?"
    has_special = any(c in special_characters for c in password)
    if has_special:
        score += 1
    else:
        suggestions.append("Include special symbols (!@#$%^&*...).")

    checklist = [
        ("Length (8+ characters)", has_length),
        ("Uppercase Characters (A-Z)", has_upper),
        ("Lowercase Characters (a-z)", has_lower),
        ("Numerical Digits (0-9)", has_digit),
        ("Special Symbols (!@#$)", has_special)
    ]

    UI.strength_display(score, checklist, suggestions if suggestions else None)
    if score == 5:
        UI.success("Hardened Credential: This password satisfies all primary complexity checks.")
    elif score >= 3:
        UI.info("Acceptable Credential: Meets baseline requirements, but could be hardened.")
    else:
        UI.warning("Weak Credential: Vulnerable to credential stuffing or dictionary attacks.")