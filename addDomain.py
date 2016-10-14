#!/usr/bin/python3

import sys, getopt
import os
import shutil

serverEmail = 'example@example.com'
website = None

def main(argv):
    checkRunAsRoot()

    domain = None
    subdomain = None
    global website

    try:
        opts, args = getopt.getopt(argv, "hd:s:", ["domain=","subdomain="])
    except getopt.GetoptError as error:
        print("\033[91mError: " + str(error) + " \033[0m")
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-d", "--domain"):
            domain = arg
        elif opt in ("-s", "--subdomain"):
            subdomain = arg

    if not domain:
        usage()
        sys.exit()

    if not subdomain:
        website = str(domain)
    else:
        website = str(subdomain) + str(".") + str(domain)

    path = makedirs(domain, subdomain)
    makeApacheFile(domain, path)

    services()

    print("\033[92mDone with creating website \033[0m")
    sys.exit()

def checkRunAsRoot():
    euid = os.geteuid()
    if euid != 0:
        print("Script not started as root.")
        print("Reasons to run it as root:")
        print("1: Need to restart apache")
        print("2: Need to a2ensite")
        sys.exit()

def makedirs(domain, subdomain):
    if not subdomain:
        path = str("/var/www/") + str(domain) + str("/public_html")
    else:
        path = str("/var/www/") + str(domain) + str("/subdomains/") + str(subdomain) + str("/public_html")
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print("\033[91mError: site already exits \033[0m")
        question = input('Override/clean this domain [y/n] ')
        if question.lower() == 'y':
            print("Overriding directory")
            shutil.rmtree(path)
            os.makedirs(path)
        else:
            sys.exit()
    #shutil.chown(path, user=www-data, group=www-data)
    return path

def makeApacheFile(domain, path):
    print(website)
    text = """<VirtualHost *:80>
        ServerAdmin """ + str(serverEmail) + """
        ServerName """ + str(domain) + """
        ServerAlias """ + str(website) + """
        DocumentRoot """ + str(path) + """
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
    </VirtualHost>"""

    apacheFile = open("/etc/apache2/sites-available/" + str(website) + '.conf', 'w')

    apacheFile.write(text)

    apacheFile.close()

def services():
    addSiteCommand = str("a2ensite ") + str(website) + str(".conf")
    restartApacheCommand = str("service apache2 restart")
    os.system('%s' % (addSiteCommand))
    print("Adding " + str(website) + " to apache")

    os.system('%s' % (restartApacheCommand))
    print("Restarting apache")

def usage():
    print("Usage: test.py -d <domain> [-s <subdomain>]")

if __name__ == "__main__":
   main(sys.argv[1:])
