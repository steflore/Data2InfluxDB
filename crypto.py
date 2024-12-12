import sys
import pwinput
import os
from cryptography.fernet import Fernet

def main(run_from_script=True, username: str='', password: str=''):
    if os.path.exists('.key.file'):
        if run_from_script:
            new_key = input("Existing key file - do you wish to use it (ENTER defaults to 'y')?\r\nNote: Answering 'n' will " \
                            "result in a new key being generated.  Any existing encrypted usersnames/passwords will need to " \
                            "be replaced by new ones generated from the new key (y|n): ")
            if new_key.lower() == 'y':
                key_file = open('.key.file', 'r')
                key = key_file.read().encode('ASCII')
                key_file.close()
            elif new_key.lower() == 'n':
                key = Fernet.generate_key()
                key_file = open('.key.file', 'w')
                key_file.write(key.decode('ASCII'))
                key_file.close()
                print('REMEMBER YOU WILL NEED TO REPLACE EXISTING ENCRYPTED USERNAMES/PASSWORDS WITH NEW ONES GENERATED ' \
                      'FROM THIS NEW KEY, AS THEY WILL NO LONGER WORK.')
            elif new_key == "":
                key_file = open('.key.file', 'r')
                key = key_file.read().encode('ASCII')
                key_file.close()
            else:
                sys.exit("Invalid option - Only y|n is acceptable")
        else:
            # Using existing key since this was called.  Expectation is there should be no existing key since calling
            # the script only happens from installer.py which only runs during initial build of a new server.
            key_file = open('.key.file', 'r')
            key = key_file.read().encode('ASCII')
            key_file.close()
    else:
        key = Fernet.generate_key()
        key_file = open('.key.file', 'w')
        key_file.write(key.decode('ASCII'))
        key_file.close()
    if key:
        try:
            cipher_suite = Fernet(key)
        except ValueError:
            sys.exit("The key isn't valid")
    else:
        sys.exit('No key found in file')

    cipher_suite = Fernet(key)
    if run_from_script:
        user = input('Enter username: ').encode('ASCII')
        if user:
            ciphered_user = cipher_suite.encrypt(user)
        else:
            sys.exit("No username entered")
        password = pwinput.pwinput(prompt='Password: ', mask='*')
        if password:
            ciphered_password = cipher_suite.encrypt(password.encode('ASCII'))
        else:
            sys.exit("No password entered")
    else:
        # We use the passed in username/password to generate encrypted versions
        ciphered_user = cipher_suite.encrypt(username.encode('ASCII'))
        ciphered_password = cipher_suite.encrypt(password.encode('ASCII'))

    if run_from_script:
        print('username:', ciphered_user.decode('ASCII'))
        print('password:', ciphered_password.decode('ASCII'))
    else:
        return [ciphered_user.decode('ASCII'), ciphered_password.decode('ASCII')]
if __name__ == '__main__':
    main()
else:
    main(run_from_script=False)