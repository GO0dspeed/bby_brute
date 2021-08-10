import argparse
from sys import exit
from brute import Brute


def define_arguemnts():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-u", "--userfile", help="Path to user file", required=True)
    parser.add_argument("-p", "--passfile", help="Path to password file", required=True)
    parser.add_argument("-t", "--type", help="Type of service to brute force", choices=["ssh", "ad", "ssh,ad", "ad,ssh"])
    parser.add_argument("-d", "--domain", help="Domain to use for LDAP", required=False)
    parser.add_argument("-v", "--verbose", help="Verbose output (prints all attempts", action="store_true", required=False)
    parser.add_argument("-q", "--quit-on-success", help="Quit on successful login", action="store_true", required=False)
    return parser,parser.parse_args()

def main():
    print("""
          _____________,-.___     _
     |____        { {]_]_]   [_]
     |___ `-----.__\ \_]_]_    . `
     |   `-----.____} }]_]_]_   ,
     |_____________/ {_]_]_]_] , `
                   `-'
        """)
    parser, args = define_arguemnts()
    if (args.type == "ad" or args.type == "ad,ssh" or args.type == "ssh,ad") and not args.domain:
        print(f"{parser.print_help()}Error: LDAP selected without a domain provided")
        exit(0)
    action = Brute(args.target, args.userfile, args.passfile, args.type, args.domain, args.verbose, args.quit_on_success)
    action.main_loop()


if __name__ == "__main__":
    main()
