# HL7Extract

HL7Extract is an open-source Python framework for transforming raw HL7 v2.x message streams into structured, analysis-ready datasets. It is designed to support clinical data analysis, interoperability workflows, and downstream applications such as quality reporting, research, and machine learning.

---

## Overview

HL7 v2.x messages are widely used in healthcare systems but are often difficult to work with directly due to their hierarchical structure, repetitive patterns, and variability across implementations.

HL7Extract provides a flexible and extensible approach to:
- Parse HL7 message streams  
- Extract fields, components, and subcomponents  
- Normalize data into structured formats  
- Enable downstream analysis and reporting  

---

## Motivation

Clinical data stored in HL7 messages is rich but not immediately usable for analytics. Extracting meaningful, consistent data from these messages typically requires custom parsing logic and deep knowledge of the HL7 specification.

HL7Extract was developed to bridge the gap between raw clinical message streams and structured datasets that can be easily queried, analyzed, and modeled.

---

## Use Cases

- Clinical data analysis and reporting  
- HL7 interface validation and troubleshooting  
- Regulatory reporting (e.g., syndromic surveillance)  
- Data preparation for machine learning and statistical modeling  
- EHR data extraction for research and study design  

---

## Features

- HL7 v2.x message parsing  
- Configurable field extraction using JSON notation
- Support for:
  - Segment repetition  
  - Field repetition  
  - Components and subcomponents  
- Flexible mapping definitions for custom extraction logic  
- Designed for integration into Python-based data pipelines  

---

## Example

### Input (HL7 Message)

MSH|^~\&|TEST_APP|TEST_FAC|EXTRACTOR|DEV|20260424071500||ADT^A01^ADT_A01|MSG000001|P|2.5.1
EVN|A01|20260424071500|||^ADAMS^JULIA^^^^^^NPI
...

### Extraction Configuration

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

### Output

mark@drop1:~/src/HL7Extract$ python3 -m pdb ./extract_example.py msh_example.json msh_example.hl7
> /home/mark/src/HL7Extract/extract_example.py(3)<module>()
-> from hl7_extract import HL7Extract
(Pdb) n
> /home/mark/src/HL7Extract/extract_example.py(4)<module>()
-> import sys
(Pdb) 
> /home/mark/src/HL7Extract/extract_example.py(6)<module>()
-> if len(sys.argv) < 3:
(Pdb) 
> /home/mark/src/HL7Extract/extract_example.py(10)<module>()
-> extr = HL7Extract(sys.argv[1], sys.argv[2])
(Pdb) 
> /home/mark/src/HL7Extract/extract_example.py(11)<module>()
-> ret = extr.extract_all_hl7()
(Pdb) 
> /home/mark/src/HL7Extract/extract_example.py(13)<module>()
-> for key in ret:
(Pdb) p extr.hl7_msg
[[['MSH'], ['|'], ['^~\\&'], ['TEST_APP'], ['TEST_FAC'], ['EXTRACTOR'], ['DEV'], ['20260424071500'], [''], [[['ADT'], ['A01'], ['ADT_A01']]], ['MSG000001'], ['P'], ['2.5.1']], [['EVN'], ['A01'], ['20260424071500'], [''], [''], [[[''], ['ADAMS'], ['JULIA'], [''], [''], [''], [''], [''], ['NPI']]]]]
(Pdb) p extr.hl7_msg['MSH']
[[['MSH'], ['|'], ['^~\\&'], ['TEST_APP'], ['TEST_FAC'], ['EXTRACTOR'], ['DEV'], ['20260424071500'], [''], [[['ADT'], ['A01'], ['ADT_A01']]], ['MSG000001'], ['P'], ['2.5.1']]]
(Pdb) p ret
{'Trigger_Event': 'A01'}
---

## Installation

```bash
git clone https://github.com/markcsmith78/HL7Extract.git
```

---

## Usage

```python
from hl7extract import HL7Extract

extractor = HL7Extract("mapping.json", "input.hl7")
result = extractor.extract_all_hl7()

print(result)
```

---

## Design Principles

- **Specification-aware**: Built around HL7 v2.x structure and notation  
- **Config-driven**: Extraction logic defined externally via mappings  
- **Extensible**: Designed to support additional transformations and output formats  
- **Analysis-focused**: Prioritizes structured output suitable for downstream analytics  

---

## Roadmap

- JSON configurable output, behavior
- Validation against HL7 profiles/specifications  
- Hierarchical element processing (if one doesn't succeed, try the next)
- Project-specific configuration files (NSSP, HDC, etc)

---

## Real-World Context

This project was developed in a hospital environment to investigate HL7 message noncompliance, support regulatory reporting, and enable analysis of clinical workflows and system integrations.

---

## Contributing

Contributions are welcome. Please open an issue or submit a pull request with proposed changes.

---

## License

GNU

