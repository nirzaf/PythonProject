#!/usr/bin/env python3
"""
Test script for HL7 to JSON Converter
"""

import sys
import json
from main import HL7Converter

def main():
    """Test the HL7 to JSON converter with a sample message"""
    # Sample HL7 message from the MD file
    sample_message = r"""MSH|^~\&|Millennium|HMC|RHAPSODY_ADT|HMC|20250601083201||ADT^A31|Q8818940207T16062243286|P|2.3||||||8859/1
EVN|A31|20250601083201|||MCHANDA^Chanda^Mahanteshwar^^^Mr.^^^CCV Username^Personnel^^^USERID^""
PID|1||HC09193054^^^MRN^MR^""||QAT^HOMECARETEST^^^^^official||19800508|male||National|^^^""^^Qatar^Home^^""~^^^""^^""^Birth^^""~mahanteshportal11@gmail.com^^^""^^""^E-mail^^""||333333^Pager personal^""~||Arabic|Married|""||28675678654|||||||||Qatari
PV1||
OBX|1|CE|REGFACILITY||HG Hamad||||||
OBX|2|CE|COUNTRY_RES||Qatar||||||
OBX|3|DT|QATAR_ID_EXP||20310531||||||
OBX|4|CE|PHCC_GEN_CON||Yes||||||
OBX|5|CE|PREF_LANGUAG||Arabic||||||"""

    # Convert the message to JSON
    json_data, error = HL7Converter.convert_hl7_to_json(sample_message)

    if error:
        print(f"Error: {error}")
    else:
        print("\nFinal JSON output:")
        print(json.dumps(json_data, indent=2))

if __name__ == "__main__":
    main()
