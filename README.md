# Stat-utils

This package is aselections of various utils for statistics.
It is inspired by R functions and packages.

## Usage

### Adjust p values for multiple comparisons
```python
p = [0.005, 0.04, 0.01, 0.5, 0.01, 0.7]
p_adjusted = p_adjust(p, method='holm')
```

Supported methods for multiple comparison:
- Bonferroni
- Holm-Bonferroni
- Hochberg
- Hommel
- BH
- BY
- none

