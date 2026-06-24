def calculate_tax(income):
    if income <= 60000:
        return 0
    elif income <= 200000:
        return (income - 60000) * 0.10
    elif income <= 400000:
        return 14000 + (income - 200000) * 0.15
    else:
        return 44000 + (income - 400000) * 0.20
