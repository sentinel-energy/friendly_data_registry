---
name: Add value/index column to registry
about: Suggest the schema for a new column to be included in the registry
title: ''
labels: new-column
assignees: ''

---

Please check your suggested addition is in the YAML format, and
matches the following properties.  For a complete list of all
supported properties, see the [frictionless
documentation](https://specs.frictionlessdata.io/table-schema/).

```
name: <column_name>
type: <type>
constraints:  # optional
  ...
description: >-
  Free text description of your column.  This can include markdown syntax to for
  simple formatting.  The text here will be included in the online documentation.
```

### Location

Ensure your suggested column schema is in the correct directory.
- value column: [`cols`](https://github.com/sentinel-energy/friendly_data_registry/tree/master/friendly_data_registry/cols), 
- index column: [`idxcols`](https://github.com/sentinel-energy/friendly_data_registry/tree/master/friendly_data_registry/idxcols)
