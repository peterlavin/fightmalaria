import SOAPpy, urllib
from SOAPpy import WSDL, SOAPProxy
#wsdlfile = '/home/lavinp/workspace/SocialGridAgents/skeletons/gt4/schema/examples/TmpBoincPaService_instance/TmpBoincPa.wsdl'
#data = urllib.urlopen(wsdlfile).read()
#print data
url = 'https://192.168.18.11:8443/wsrf/services/examples/core/tmpBoincPa/TmpBoincPaService'
#sp = 'urn:testIsFilePresent'
nsp = 'urn:testRemoteSysExec'
ma=''
hd=''
sa=''

#headers = SOAPpy.Types.headerType()
pa_server=SOAPProxy(url, namespace=nsp)
#pa_server=SOAPProxy(url)
#pa_server.config.dumpSOAPOut = True
#pa_server.config.dumpSOAPIn = True
file = '/tmp/presentfile'
print pa_server.isFilePresentRequest(file)
#print pa_server.testRemoteSysExec()
