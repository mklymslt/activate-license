#!/usr/bin/env python
'''
----------------------------------------------------------------------------
The contents of this file are subject to the "END USER LICENSE AGREEMENT FOR F5
Software Development Kit for iControl"; you may not use this file except in
compliance with the License. The License is included in the iControl
Software Development Kit.

Software distributed under the License is distributed on an "AS IS"
basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See
the License for the specific language governing rights and limitations
under the License.

The Original Code is iControl Code and related documentation
distributed by F5.

The Initial Developer of the Original Code is F5 Networks,
Inc. Seattle, WA, USA. Portions created by F5 are Copyright (C) 1996-2004 F5 Networks,
Inc. All Rights Reserved.  iControl (TM) is a registered trademark of F5 Networks, Inc.

Alternatively, the contents of this file may be used under the terms
of the GNU General Public License (the "GPL"), in which case the
provisions of GPL are applicable instead of those above.  If you wish
to allow use of your version of this file only under the terms of the
GPL and not to allow others to use your version of this file under the
License, indicate your decision by deleting the provisions above and
replace them with the notice and other provisions required by the GPL.
If you do not delete the provisions above, a recipient may use your
version of this file under either the License or the GPL.
----------------------------------------------------------------------------
'''




def get_license_from_F5_License_Server ( server_hostname, dossier_string, eula_string, email,
                                         firstName, lastName, companyName, phone, jobTitle,
                                        address, city, stateProvince, postalCode, country ):

    try:

        license_string = ""
        

        download_url = "https://" + server_hostname + "/license/services/urn:com.f5.license.v5b.ActivationService?wsdl"


        local_wsdl_file_name = str(server_hostname) + '-f5wsdl-w-https.xml'
        wsdl_data = []

        try:
            with open(local_wsdl_file_name, 'r') as fh_wsdl:
                wsdl_data = fh_wsdl.read()
        except:
            print "Can't find a locally stored WSDL file."


        if not wsdl_data:
            print "Attempting to fetch wsdl online."
            f5wsdl = urllib2.urlopen(download_url)
            newlines = []
            for line in f5wsdl:
                # do the replacing here
                newlines.append(line.replace('http://' + server_hostname , 'https://' + server_hostname))

            fh_local = open(local_wsdl_file_name,'w')
            fh_local.writelines(newlines)
            fh_local.close()

        
        url = "file:" + urllib.pathname2url(os.getcwd()) + "/" +  local_wsdl_file_name

        
        client = Client(url)

        

        transaction = client.factory.create('tns1:LicenseTransaction')
        # If eula isn't present on first call to getLicense, transaction will fail
        # but it will return a eula after first attempt
        transaction = client.service.getLicense(
                                                dossier = dossier_string,
                                                eula = eula_string,
                                                email = email,
                                                firstName = firstName ,
                                                lastName = lastName,
                                                companyName = companyName,
                                                phone = phone,
                                                jobTitle = jobTitle,
                                                address = address,
                                                city = city,
                                                stateProvince = stateProvince,
                                                postalCode = postalCode,
                                                country = country,
                                                )

        #Extract the eula offered from first try
        eula_string = transaction.eula

        if transaction.state == "EULA_REQUIRED":
            #Try again, this time with eula populated
            transaction = client.service.getLicense(
                                                        dossier = dossier_string,
                                                        eula = eula_string,
                                                        email = email,
                                                        firstName = firstName ,
                                                        lastName = lastName,
                                                        companyName = companyName,
                                                        phone = phone,
                                                        jobTitle = jobTitle,
                                                        address = address,
                                                        city = city,
                                                        stateProvince = stateProvince,
                                                        postalCode = postalCode,
                                                        country = country,
                                                        )

        if transaction.state == "LICENSE_RETURNED":
            license_string = transaction.license
        else:
            print "Can't retrieve license from Licensing server"
            print "License server returned error: Number:" + str(transaction.fault.faultNumber) + " Text: " + str(transaction.fault.faultText)

        return license_string

    except:
        print "Can't retrieve License from Server"
        traceback.print_exc(file=sys.stdout)

### IMPORT MODULES ###
import os
import sys
import time
import traceback
import base64
import urllib
import urllib2
import getpass
from suds.client import Client
from optparse import OptionParser

import bigsuds



#### SET CONFIG VARIABLES ####


#Misc EULA Variables
email  = "example.icontrol@f5.com"
firstName = "example"
lastName = "iControl"
companyName = "F5"
phone = "2062725555"
jobTitle = "DEV OPS"
address = "111 EXAMPLE ICONTROL RD"
city = "Seattle"
stateProvince = "WA"
postalCode = "98119"
country = "United States"
eula_string = ""

#F5 Licensing Server Hostname Variable
server_hostname = "activate.f5.com"

########## START MAIN LOGIC ######

dossier_string = sys.argv[1]



license_string = get_license_from_F5_License_Server(
server_hostname,
dossier_string,
eula_string,
email,
firstName,
lastName,
companyName,
phone,
jobTitle,
address,
city,
stateProvince,
postalCode,
country
)

if license_string:
	print "License Found"
	print (license_string)

else:
	print "Sorry. Could not retrieve License. Check your connection"
