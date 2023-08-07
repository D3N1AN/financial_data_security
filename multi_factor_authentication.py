import pyotp

def generate_totp_secret():
    # Generate a random secret key
    return pyotp.random_base32()

def generate_totp_uri(secret, account_name):
    # Generate the TOTP URI for the specific account
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=account_name, issuer_name="My Company")

def verify_totp_token(secret, token):
    # Verify if the TOTP token is valid
    totp = pyotp.TOTP(secret)
    return totp.verify(token)

if __name__ == "__main__":
    # Example usage
    secret = generate_totp_secret()
    account_name = "john.doe@example.com"

    totp_uri = generate_totp_uri(secret, account_name)
    print("Scan the following QR code using a TOTP app:")
    print(totp_uri)
    token = input("Enter the TOTP token: ")
    is_valid = verify_totp_token(secret, token)
    if is_valid:
        print("Token is valid.")
    else:
        print("Token is invalid.")
