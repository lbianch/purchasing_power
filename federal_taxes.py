def standard_deduction(family_size):
    personal = 4050 * family_size
    standard = 6300
    if family_size > 2:
        standard *= 2
    return personal + standard


def tax(net_income):
    if net_income > 466950:
        return 130578 + 0.396 * (net_income - 466950)
    if net_income > 413350:
        return 111818 + 0.35 * (net_income - 413350)
    if net_income > 231450:
        return 51791 + 0.33 * (net_income - 231450)
    if net_income > 151900:
        return 29517 + 0.28 * (net_income - 151900)
    if net_income > 75300:
        return 10367 + 0.25 * (net_income - 75300)
    if net_income > 18550:
        return 1855 + 0.15 * (net_income - 18550)
    if net_income < 0:
        return 0.0
    return 0.10 * net_income


def FICA(gross_income):
    return 0.0765 * min(118500, gross_income)


def taxes(gross_income, family_size):
    return tax(gross_income - standard_deduction(family_size)) + FICA(gross_income)
