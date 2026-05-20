# HL7Extract Configuration File

HL7Extract uses a JSON-formatted configuration file to control program behavior.

The configuration file specifies:

- Output destinations
- Output formatting
- Network settings
- Future AI integration settings

Example configuration file:

```json
{
  "version": "1.0",

  "output": {
    "enabled": true,
    "destinations": [
      {
        "type": "terminal",
        "enabled": true,
        "format": "key_value"
      },
      {
        "type": "csv",
        "enabled": false,
        "path": "output/hl7extract.csv",
        "format": "extracted_elements",
        "include_header": true,
        "append": true
      }
    ]
  },

  "ai": {
    "enabled": false,
    "provider": "openai",
    "model": "gpt-5.2",
    "use_on": [
      "extracted_elements"
    ],
    "tasks": [
      "summarize"
    ],
    "send_phi": false
  }
}
```

---

# Top-Level Configuration Sections

| Section | Description |
|---|---|
| `version` | Configuration format version |
| `output` | Output configuration |
| `ai` | AI integration configuration |

---

# Output Configuration

The `output` section controls where extracted HL7 data is sent and how it is formatted.

## Example

```json
"output": {
  "enabled": true,
  "destinations": [
    {
      "type": "terminal",
      "enabled": true,
      "format": "key_value"
    }
  ]
}
```

---

# Output Destinations

The `destinations` field is an array. Multiple destinations may be used simultaneously.

Example:

```json
"destinations": [
  {
    "type": "terminal",
    "enabled": true,
    "format": "key_value"
  },
  {
    "type": "csv",
    "enabled": true,
    "path": "output/results.csv",
    "format": "json"
  }
]
```

---

# Destination Types

## Terminal Output

Outputs extracted data to the console.

Example:

```json
{
  "type": "terminal",
  "enabled": true,
  "format": "key_value"
}
```

---

## CSV Output

Outputs extracted data to a CSV file.

Example:

```json
{
  "type": "csv",
  "enabled": true,
  "path": "output/results.csv",
  "format": "extracted_elements",
  "include_header": true,
  "append": true
}
```

### CSV Fields

| Field | Description |
|---|---|
| `path` | CSV output file path |
| `include_header` | Write CSV header row |
| `append` | Append to existing file |

---

## Network Output

Outputs extracted data to a network destination.

Example:

```json
{
  "type": "network",
  "enabled": true,
  "host": "127.0.0.1",
  "port": 9000,
  "protocol": "tcp",
  "format": "json"
}
```

### Network Fields

| Field | Description |
|---|---|
| `host` | Destination hostname or IP |
| `port` | Destination port |
| `protocol` | `tcp` or `udp` |

---

# Output Formats

The `format` field controls how extracted data is rendered.

| Format | Description |
|---|---|
| `key_value` | Key/value formatted output |
| `extracted_elements` | Only extracted HL7 elements |
| `json` | JSON-formatted output |
| `csv_row` | CSV-compatible row format |
| `raw` | Raw HL7 message output |

---

# AI Configuration

The `ai` section controls optional AI integration features.

Example:

```json
"ai": {
  "enabled": true,
  "provider": "openai",
  "model": "gpt-5.2",
  "use_on": [
    "extracted_elements"
  ],
  "tasks": [
    "summarize",
    "classify"
  ],
  "send_phi": false
}
```

---

# AI Fields

| Field | Description |
|---|---|
| `enabled` | Enable AI processing |
| `provider` | AI provider |
| `model` | AI model name |
| `use_on` | Which data to send to AI |
| `tasks` | AI tasks to perform |
| `send_phi` | Allow PHI to be sent to AI |

---

# AI Tasks

| Task | Description |
|---|---|
| `summarize` | Generate message summaries |
| `classify` | Categorize messages |
| `detect_missing_fields` | Detect missing required data |
| `explain_message` | Explain message contents |
| `extract_insights` | Generate analytical insights |

---

# Configuration Validation

HL7Extract supports JSON Schema validation for configuration files.

Validation ensures:

- Required fields exist
- Values are valid
- Invalid destination types are rejected
- Invalid formats are rejected

---

# Notes

- Multiple output destinations may be enabled simultaneously
- Unknown configuration fields are rejected
- Future versions may introduce additional destination and AI types
- AI features are optional and disabled by default
- PHI handling should be reviewed carefully before enabling AI processing
