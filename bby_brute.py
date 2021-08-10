from brute import Brute
import argparse

def define_arguemnts():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-u", "--userfile", help="Path to user file", required=True)
    parser.add_argument("-p", "--passfile", help="Path to password file", required=True)
    parser.add_argument("-t", "--type", help="Type of service to brute force", choices=["ssh", "ad", "ssh,ad", "ad,ssh"])
    parser.add_argument("-d", "--domain", help="Domain to use for LDAP", required=False)
    parser.add_argument("-v", "--verbose", help="Verbose output (prints all attempts", action="store_true", required=False)
    parser.add_argument("--quit-on-success", help="Quit on successful login", required=False)
    return parser.parse_args()

def main():
    print("""
          _____________,-.___     _
     |____        { {]_]_]   [_]
     |___ `-----.__\ \_]_]_    . `
     |   `-----.____} }]_]_]_   ,
     |_____________/ {_]_]_]_] , `
                   `-'
        """)
    args = define_arguemnts()
    action = Brute(args.target, args.userfile, args.passfile, args.type, args.domain, args.verbose, args.quit_on_success)
    try:
        action.main_loop()
    except Exception as e:
        print(f"An Error Occured\n{e}")

if __name__ == "__main__":
    main()
