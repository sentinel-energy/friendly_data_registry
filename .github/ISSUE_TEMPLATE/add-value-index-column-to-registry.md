---
name: Add value/index column to registry
about: Suggest the schema for a new column to be included in the registry
title: ''
labels: new-column
assignees: ''

---

<!-- The text below is for guidance, please remove before submitting the issue -->

Please check your suggested addition matches the following properties.
For a complete list of all supported properties, see the [frictionless
documentation](https://specs.frictionlessdata.io/table-schema/).

```
name: <column_name>
type: <type>
constraints:  # optional
  ...
description: >-
  Free text description of the column.  This can include restructured
  text markup for simple formatting.  The text here will be included in
  the online documentation.
```

You can find more documentation on how to add a new column in the
Friendly data registry
[documentation](https://sentinel-energy.github.io/friendly_data/registry.html).

### Where to add the new column

Ensure the suggested column schema is in the correct directory.
- value column: [`cols`](https://github.com/sentinel-energy/friendly_data_registry/tree/master/friendly_data_registry/cols)
- index column: [`idxcols`](https://github.com/sentinel-energy/friendly_data_registry/tree/master/friendly_data_registry/idxcols)

<!-- The text above is for guidance, please remove before submitting the issue -->
