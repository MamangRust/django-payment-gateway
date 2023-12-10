import random


def unique_order_number():
    random_order_number = str(random.random())[2:]
    get_random_order_number = int("4" + random_order_number)
    get_digit_order_number = "".join(filter(str.isdigit, str(get_random_order_number)))
    result_digit_order_number = (
        int(get_digit_order_number) if get_digit_order_number.isdigit() else None
    )
    return (
        f"bfc-{result_digit_order_number}"
        if result_digit_order_number is not None
        else None
    )
