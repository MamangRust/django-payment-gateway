def payment_method_validator(payment_method):
    payment_rules = [
        "alfamart",
        "indomart",
        "lawson",
        "dana",
        "ovo",
        "gopay",
        "linkaja",
        "jenius",
        "fastpay",
        "kudo",
        "bri",
        "mandiri",
        "bca",
        "bni",
        "bukopin",
        "e-banking",
        "visa",
        "mastercard",
        "discover",
        "american express",
        "paypal",
    ]

    return payment_method.lower() in payment_rules
