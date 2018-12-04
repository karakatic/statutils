# statutils

This package is aselections of various utils for statistics.
It is inspired by R functions and packages.

## Usage

### Adjust p values for multiple comparisons
Use `p_adjust` method to adjust p-values with Bonferroni correction, Holm-Bonferroni correction or others. `p_adjust` is a rewrite of R's `p.adjust` function with the numpy arrays.
Use it in the same way.

Supported methods for multiple comparison (`method` argument):
- `bonferroni` Bonferroni correction
- `holm` Holm (1979)
- `hochberg` Hochberg (1988)
- `hommel` Hommel (1988)
- `BH` Benjamini & Hochberg (1995)
- `BY` Benjamini & Yekutieli (2001)
- `none` as a pass-through option



#### Example
```python
from statutils.multi_comparison import p_adjust

p = [0.005, 0.04, 0.01, 0.5, 0.01, 0.7]
p_adjusted = p_adjust(p, method='holm')
```


