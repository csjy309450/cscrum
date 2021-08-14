import xml.sax
import xml.sax.handler


class XMLHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.buffer = ""
        self.mapping = {}

    def startElement(self, name, attributes):
        self.buffer = ""

    def characters(self, data):
        self.buffer += data

    def endElement(self, name):
        self.mapping[name] = self.buffer

    def getDict(self):
        return self.mapping


data = "<type><ref refid=\"test_8h_1ad50602a3ef40bd7a6c81f4b245921380\" kindref=\"member\">NET_DVR_API</ref> <ref refid=\"test_8h_1a9154c0d0c21af4686624543215b4e5f2\" kindref=\"member\">LONG</ref> <ref refid=\"test_8h_1ad16f14718feefaa629b3b7601ac9fdeb\" kindref=\"member\">__stdcall</ref></type>"

strxml = data.find("<>")

xh = XMLHandler()
xml.sax.parseString(data.encode('utf-8'), xh)
ret = xh.getDict()
pass