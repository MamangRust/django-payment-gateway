def rupiah_formatter(digit):
    digit_number = int(digit)
    formatted = (
        f"Rp {digit_number:,.0f}"  # Format the number with comma as thousand separators
    )
    return formatted
