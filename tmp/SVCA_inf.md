# SVCA module information



Standards information:

NIST 800-37 rev.2

NIST 800-53 rev.5

FIPS 200

FIPS 199



https://www.cvedetails.com

https://www.cisecurity.org/cis-benchmarks/

https://oval.cisecurity.org/



Programmatically keep up with security vulnerability information via REST APIs to build tools and assess the impact of security vulnerabilities:



Cisco API:  https://developer.cisco.com/psirt/

Cisco WEB: https://tools.cisco.com/security/center/publicationListing.x



Palo Alto WEB: https://securityadvisories.paloaltonetworks.com



Juniper WEB: https://kb.juniper.net/InfoCenter/index?page=content&channel=SECURITY_ADVISORIES



IDS:

https://suricata-ids.org

CIS Albert: https://gcn.com/articles/2018/03/28/albert-intrusion-detection-voter-registration.aspx



Vulnerability Base:

NVD: https://nvd.nist.gov/vuln/data-feeds



# The Most Popular Security Assessment and Server Hardening Tools

https://opensourceforu.com/2015/06/the-most-popular-security-assessment-and-server-hardening-tools/



SCAP vs CIS-CAT ib nasa

https://www.nccs.nasa.gov/sites/default/files/Poster_Jordan_CaraballoVega_Greenbelt_CompScienceIT.pdf

[Open-scap] using openscap with CIS benchmark:

https://www.redhat.com/archives/open-scap-list/2015-July/msg00010.html



xccdf
https://habr.com/ru/company/pt/blog/141869/



oval
https://habr.com/ru/post/136046/



swid (software id)
https://en.wikipedia.org/wiki/ISO/IEC_19770



windows 3rd party scan and update tools

https://www.howtogeek.com/howto/5529/how-to-keep-your-new-windows-7-computer-updated-and-secure/#comments



https://patchmypc.com/home-updater-download





powershell command for versionn check for dll file ssleay32.dll: 

Get-ChildItem c:\"Program Files (x86)"\ -include ssleay32.dll -recurse | foreach-ob
ject { "{0}" -f [System.Diagnostics.FileVersionInfo]::GetVersionInfo($_) }



CIS-CAT leakings:

- remote scanning not for all systems (for Cisco only?)
- slow interface
- start .bat after that start .jar (not convenient)



About Scanners:

https://habr.com/ru/company/echelon/blog/347702/

https://ru.wikipedia.org/wiki/Metasploit

https://www.kali.org



CIS Windows 2010

https://cdn2.hubspot.net/hubfs/2101505/CIS%20Controls%20Microsoft%20Windows%2010%20Cyber%20Hygiene%20Guide.pdf?__hssc=183371129.6.1563356943280&__hstc=183371129.53c4e62f69206985a9b46d64ad8ba2f1.1561732804532.1563353995575.1563356943280.11&__hsfp=1711008685&hsCtaTracking=0cd3e3d7-1f26-467d-a63d-fb4783c5ecde%7C93d6bfd4-cb4d-4377-a87b-50d88dc8f449



WPS

https://helpugroup.ru/vzlom-pin-koda-wps-dlya-polucheniya-parolya-pri-pomoshhi-bully/



Scaner Nessus



https://networkguru.ru/tenable-nessus-vulnerability-scanner/



open source scanner: OpenVAS



For WiFi: AirCrack

Web scanners: Nessus, Acunetix, 
Open Source: Nikto, Wapiti, Burp Suite proxy tool



DataBase Scanner: sqlmap (open source)

Penetration tests: Metasploit



-----------

NIST Configuration classification standart:

CCE: Common ConfigurationEnumeration

------------

