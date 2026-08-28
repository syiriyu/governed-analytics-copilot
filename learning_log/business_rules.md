Contract start dates are generated at contract level rather than customer level, because a customer can acquire different products at different times.

Renewal eligibility is derived from contract dates rather than randomly generated

Renewal outcome itself is deferred because later customer usage and support behaviour will influence synthetic churn

For revenue one row = one contract in one month

### Derived data vs. generated data

customer attributes and contract assignments contain synthetic randomness

Monthly revenue does not need additional randomness because it can be derived from contract values and dates

Where possible, derived values are preferable to independently generated values because they preserve internal consistency

Synthetic data validation has two levels:

1. Technical validation
   Did the generated data reflect the rules encoded in the generator?

2. Business validation
   Are those encoded assumptions/distributions themselves plausible?

Example:
The ~50% SLA breach rate is technically expected given the current
lognormal generation logic, but may be too high for a plausible
business scenario.

Satisfaction validation behaved as designed:
non-breached ≈ 4.3 and breached ≈ 3.0.