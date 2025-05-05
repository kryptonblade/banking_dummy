
from auth import register_user, confirm_registration, login, reset_password, confirm_reset_password
from account import add_account_to_user, deposit, view_balance, transfer_between_own_accounts, interbank_transfer, generate_pdf_statement
from admin import authenticate_admin, list_users

if __name__ == '__main__':
    # R1 & R2: Registration
    print(register_user('user@example.com', '1234567', 'password123'))
    # this is valid email and invalid phone number , need to give error
    otp = input("Enter OTP: ")
    print(confirm_registration('user@example.com', otp))

    # Link second account for R6–R10 tests
    print(add_account_to_user('user@example.com', '9876543210'))

    # Seed balances
    print(deposit('1234567890', 2000.0))
    print(deposit('9876543210', 500.0))

    # R3: Login
    print("Login Success?", login('user@example.com', 'password123'))

    # R4: Password reset
    print(reset_password('user@example.com'))
    otp2 = input("Enter reset OTP: ")
    print(confirm_reset_password('user@example.com', otp2, 'newpass123'))

    # R5: View balance
    print("Balance:", view_balance('1234567890'))

    # R6: Own-account transfer
    print(transfer_between_own_accounts('1234567890', '9876543210', 1000.0))

    # R7: Inter-bank transfer
    print(interbank_transfer('1234567890', '9876543210', 1000.0))

    # R8: Statement download
    print(generate_pdf_statement('1234567890'))

    # R9: High-value notification
    # print(interbank_transfer('1234567890', '9876543210', 50000.0))

    # R10: Admin manage
    if authenticate_admin('admin', 'password123'):
        print("All users:", list_users())