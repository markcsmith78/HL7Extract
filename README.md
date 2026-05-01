# HL7 Extract

A lightweight Python-based engine for parsing and extracting structured
data from HL7 v2.x messages.

## Overview

HL7 Extract is designed to process raw HL7 messages and convert them
into structured, usable data formats. It supports configurable
extraction logic, making it flexible for different healthcare
integration needs.

## Features

-   Parse HL7 v2.x messages
-   Handle repeating segments and fields 
-   Configurable extraction rules via JSON
-   Clean, extensible Python architecture

## Example HL7 Input

    MSH|^~\&|EMR|HOSPITAL|LAB|HOSPITAL|202401011200||ADT^A01|12345|P|2.5.1
    PID|1||123456^^^HOSPITAL^MR||DOE^JOHN
    PV1|1|I|MEDSURG^201^A||||||||||||||||||||||||||||||||||||||||||||202401011159

## Example Configuration
Fields, components and subcomponents use a 1-based index.
[
    {
        "name" : "Admit_Date_Time", 
        "required" : "R",
        "source" : [
            {
                "notation" : "PV1-44.1",
	            "segment": "PV1",
	            "segment_repetition": 0,
	            "field": 44,
	            "field_repetition": 0,
	            "component" : 1,
	            "subcomponent": 0
            }
        ] 
    },
    {
        "name" : "Admit_Reason_Description",
        "required" : "RE",
        "source" : [ 
            {
                "notation" : "PV2-3",
	            "segment" : "PV2",
                "segment_repetition" : 0,
	            "field": 3,
                "field_repetition":0,
	            "component" : 0,
                "subcomponent" : 0
            }
        ]
    } 
]

## Example Output

    {
      "Admit_Date_Time": "202401011159",
      "Patient_ID": "123456"
    }

## Installation

Clone the repository:

    git clone https://github.com/markcsmith78/HL7Extract.git
    cd HL7Extract

Install dependencies (if applicable):

    pip install -r requirements.txt

## Usage

Run the extractor:

    python main.py input.hl7 config.json

## Project Structure

    HL7Extract/
    ├── main.py
    ├── hl7_extract.py
    ├── config/
    ├── samples/
    └── README.md

## Roadmap

-   Add support for HL7 validation
-   Expand error handling and logging
-   Support FHIR transformation
-   Add CLI flags and options

## Contributing

Contributions are welcome. Please open an issue or submit a pull
request.

## License

Specify your license here (e.g., MIT, Apache 2.0).
