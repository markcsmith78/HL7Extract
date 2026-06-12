# PacketBandit 

HL7Extract has been renamed to PacketBandit.

The project continues to focus on HL7 v2.x extraction, transformation, monitoring and healthcare interoperability.

PacketBandit is an open-source Python framework for transforming raw HL7 v2.x message streams into structured, analysis-ready datasets. It is designed to support clinical data analysis, interoperability workflows, and downstream applications such as quality reporting, validation, regulatory compliance and Electronic Lab Reporting.
To be fair, extracting fields from HL7 messages is not edge-of-your-seat exciting.  It doesn't make for good dinner convesation and it's not status update material.  But, if you're troubleshooting interfaces or analyzing large sets of HL7 messages, this is for you.  PacketBandit relieves you of the burden of counting out 'pipes' and 'hats'.  It wrassles unweildly HL7 messages that wrap several lines in your text editor into the manageable, domesticated set of fields you're interested in.  Everything else stays outside in the wild.
Configuring element extraction and PacketBandit's behavior (input/output sources) is done through JSON configuration files.  These are semantically validated against schemas before their rules are applied.  Using schema-validated extraction rules allows PacketBandit to be configured for endless different applications: Syndronic Surveillance ADT stream extraction, interfacility debugging (i.e. OBX messages from bedside monitors or medication dispensing systems), message compliance (i.e. between a local EHR and a third party system).
The latest release is Version 0.05.  It supports flat file input (MLLP framed), and can output to a terminal as key/value pairs or to a CSV file for importing into a spreadsheet application.  Schema-validation is robust and can isolate elements from the field to the subcomponent level.  Future enhancements include CSV input (commonly used between EHRs and state entities for regulatory compliance), network stream input and colorized terminal output for debugging.

---

## Overview

HL7 v2.x messages are widely used in healthcare systems but are often difficult to work with directly due to their hierarchical structure, repetitive patterns, and variability across implementations.

PacketBandit provides a flexible and extensible approach to:
- Parse HL7 message streams  
- Extract fields, components, and subcomponents  
- Normalize data into structured formats  
- Enable downstream analysis and reporting  

---

## Motivation

Clinical data stored in HL7 messages is rich but not immediately usable for analytics. Extracting meaningful, consistent data from these messages typically requires custom parsing logic and deep knowledge of the HL7 specification.

PacketBandit was developed to bridge the gap between raw clinical message streams and structured datasets that can be easily queried, analyzed, and modeled.

---

## Example Projects

### Syndromic Surveillance

Extract National Syndromic Surveillance Program required elements from ADT streams for validation and reporting.

### Clinical Device Troubleshooting

Monitor OBX messages from bedside devices for troublshooting, missing or malformed observations.

### Electronic Laboratory Reporting

Validate laboratory result messages prior to submission to public health agencies.

### Interface Development

Identify and troubleshoot discrepencies before they happen when developing an HL7 interface between a local EHR and third part system.

---

## Features

- HL7 v2.x message parsing  
- Configurable field to subcomponent extraction using JSON notation
- Support for:
  - Segment repetition  
  - Field repetition  
  - Components and subcomponents  
- Flexible mapping definitions for custom extraction logic  
- Designed for integration into Python-based data pipelines  
- CSV output
- Terminal output
- MLLP framing

---

## Example

### Input (HL7 Message)

<pre>
MSH|^~\&|TEST_APP|TEST_FAC|EXTRACTOR|DEV|20260424071500||ADT^A01^ADT_A01|MSG000001|P|2.5.1
EVN|A01|20260424071500|||^ADAMS^JULIA^^^^^^NPI
...
</pre>

### Extraction Configuration
<pre>
[    
    {
        "name"  : "Trigger_Event",
        "required" : "R",
        "source" : [
            {
                "notation" : "MSH-9.2",
                "segment" : "MSH",
                "segment_repetition" : 0,
                "field" : 9,
                "field_repetition":0,
                "component" : 2,
                "subcomponent" : 0 
            }
        ]
    }
]
</pre>

## Installation

```bash
git clone https://github.com/markcsmith78/PacketBandit.git
```

---

## Usage

```python
from hl7extract import PacketBandit 

extractor = PacketBandit("mapping.json", "input.hl7")
result = extractor.extract_all_hl7()

print(result)
```

---

## Design Principles

- **Specification-aware**: Built around HL7 v2.x structure and notation  
- **Config-driven**: Extraction logic defined externally via mappings  
- **Extensible**: Designed to support additional transformations and output formats  
- **Analysis-focused**: Prioritizes structured output suitable for downstream analytics  
- **Developer-friendly**: Command-line execution allows for pipeline integration

---

## Roadmap

- JSON configurable output, behavior (robust in v0.05)
- Validation against HL7 profiles/specifications  
- Hierarchical element processing (if one doesn't succeed, try the next)
- Project-specific configuration files (NSSP, HDC, etc)
- Network stream input
- CSV input (non MLLP framed HL7 message in cell)

---

## Real-World Context

This project was developed in a hospital environment to investigate HL7 message noncompliance, support regulatory reporting, and enable analysis of clinical workflows and system integrations.

---

## Lessons Learned

HL7 was designed to facilitate clinical communication before the explosion of technology in the healthcare sector.  Its acceptance is largely a result of it's availability -- not its design.  As a result, it is the victim of its own success.  There are several flaws in it that challenge plug-and-play integration.  
For starters, it is ambiguous.  Commonly accepted notation among industry professionals has bridged the gaps (i.e. bracketed indexs for repeating segments), but this falls short of formal specification.  Additionally, it disregards transport mechanism.  The lack of specification for transport has led to near-universal acceptance of MLLP framing, but this also falls short of formal specification and leaves the burden of transport on each individual implementation.  While not a heavy load for engineering-dominate fields, technical expertise is a limited resource in many clinical environments.  This often leaves smaller healthcare facilities at the mercy of vendors for designing and building interfaces between the facilities EHR and third party solutions.  
However, HL7 is here.  While FHIR offers solutions to these problems, it was not available when much of our current health care infrastrcture was built.  Therefore, HL7 is part of current healthcare operations and will be for years to come.  As a result, if you want to work in heathcare technology, you are likely to encounter HL7.  And that is why PacketBandit exists.

## Contributing

Contributions are welcome. Please open an issue or submit a pull request with proposed changes.

---

## License

GNU

