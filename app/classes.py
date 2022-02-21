# Classes
from logger import save_json
import json
import datetime
from flask import session
import xml.etree.cElementTree as ET
import xml.dom.minidom


class File:
    def __init__(self, name, size, extension, date, signature):
        self.name = name
        self.size = size
        self.extension = extension
        self.date = date
        self.signature = signature

    def save_info(self, base_path):
        m_encoding = 'UTF-8'

        root = ET.Element("data")
        doc = ET.SubElement(root, "file", extension=f"{self.extension}")
        ET.SubElement(doc, "name").text = f"{self.name}"
        ET.SubElement(doc, "size").text = f"{self.size}"
        ET.SubElement(doc, "uploaded_on").text = f"{self.date}"
        ET.SubElement(doc, "digital_signature").text = f"{self.signature}"

        dom = xml.dom.minidom.parseString(ET.tostring(root))
        xml_string = dom.toprettyxml()
        part1, part2 = xml_string.split('?>')
        from xml.dom import minidom
        xml_name = f"{self.name}.xml"
        save_path = f"{base_path}/{xml_name}"

        with open(save_path, 'w') as xfile:
            xfile.write(
                part1 + 'encoding=\"{}\"?>\n'.format(m_encoding) + part2)
            xfile.close()

    # Load xml info
    def load_info(email, base_path, filename, get_element, get_all=False):

        element_number = int(get_element)

        xml_name = f"{filename}.xml"
        open_path = f"{base_path}/{xml_name}"

        # Pass the path of the xml document
        tree = ET.parse(open_path)

        # get the parent tag
        root = tree.getroot()

        if get_all == False:
            element_value = root[0][element_number].text
            return element_value
        else:
            name = root[0][0].text
            size = root[0][1].text
            uploaded_on = root[0][2].text
            signature = root[0][3].text

            return name, size, uploaded_on, signature

    def update_info(filename, new_name):
        email = session['email']
        xml_path = f"static/Cloud/{email}/documents/{filename}.xml"
        xmlTree = ET.parse(xml_path)
        rootElement = xmlTree.getroot()
        for element in rootElement:
            element.find('name').text = new_name
        # Write the modified xml file.
        xmlTree.write(filename, encoding='UTF-8', xml_declaration=True)
#file = File('Test.docx', '10 MB', '.docx', '10-02-2022')
# file.save_info()


class Log:
    def __init__(self, time, location, user_ip, user_browser):
        self.time = time
        self.location = location
        self.user_ip = user_ip
        self.user_browser = user_browser

    def log_user(location, user_ip, user_browser, logName):

        time_now = datetime.now()
        file_wt = time_now.strftime('%d%m%Y-%H_%M_%S')
        email = session['email']
        upload_path = f"static/Cloud/{email}/Logs"

        # Data to be written
        dictionary = {
            "time": str(f"{file_wt}"),
            "location": str(f"{location}"),
            "user_ip": str(f"{user_ip}"),
            "user_browser": str(f"{user_browser}"),
        }

        # Serializing json
        json_object = json.dumps(dictionary, indent=4)

        # Saving json file
        new_name = f"{logName}.json"
        save_to = f"{upload_path}/{new_name}"
        with open(save_to, "a") as outfile:
            outfile.write(json_object)

        def encrypt_log():
            # RSA
            pass

        def decrypt_log():
            # RSA
            pass


def test():
    m_encoding = 'UTF-8'

    root = ET.Element("data")
    doc = ET.SubElement(root, "file", extension=".docx")
    ET.SubElement(doc, "name").text = "test.docx"
    ET.SubElement(doc, "size").text = "10 MB"
    ET.SubElement(doc, "uploaded_on").text = "10-02-2022"

    dom = xml.dom.minidom.parseString(ET.tostring(root))
    xml_string = dom.toprettyxml()
    part1, part2 = xml_string.split('?>')

    with open("FILE.xml", 'w') as xfile:
        xfile.write(part1 + 'encoding=\"{}\"?>\n'.format(m_encoding) + part2)
        xfile.close()

# test()
# File.save_info('kiki.vidovic.6969@gmail.com')


# Function testing
# value = File.load_info('kiki.vidovic.6969@gmail.com',
#                       'test2.txt', 3, get_all=False)
# print(value)
