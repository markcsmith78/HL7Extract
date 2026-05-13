# Rules for Editing/Creating JSON Files to Define Parsing Behavior

The configuration file is a JSON list of element location definitions.

This is an example of a single definition (`PV1-44.1`):

```json
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
}
```

## Required Keys

Currently, all key/value pairs must be represented.

That is, there must be a:

- `"segment"`
- `"segment_repetition"`
- `"field"`
- `"field_repetition"`
- `"component"`
- `"subcomponent"`

key, and there must be a value associated with each key.

If a key is not used, then a value of `0` is associated with it.

This applies to:

- segment repetition
- field repetition
- components
- subcomponents

If they are not used, they are assigned a value of `0`.

---

# HL7 Notation Rules

The `"notation"` key/value is not used for computation.

It acts as a human-readable representation of the element being extracted.

Since the HL7 v2.x specification is somewhat ambiguous, commonly accepted formatting conventions should be used.

## Repeated Segments

Repeated segments are represented with brackets and a zero-based index following the segment identifier.

Example:

```text
OBX[1]
```

This represents the second `OBX` segment.

---

## Fields

Fields follow a `-` after the segment.

Example:

```text
PV1-44
```

This represents the entire 44th field of the `PV1` segment.

Note that this is not affected by components. If components exist, they are all included as part of the field.

---

## Components

Components follow a `.` after the field.

Example:

```text
PV1-44.1
```

This represents the first component in the 44th field of the `PV1` segment.

---

## Subcomponents

Subcomponents follow a second `.`.

Example:

```text
PV1-44.1.1
```

This represents the first subcomponent of the first component of the 44th field of the `PV1` segment.
