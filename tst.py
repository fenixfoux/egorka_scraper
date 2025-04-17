import re


item_price = "2 699 MDL"
parsed_price = re.sub(r"[^\d]", "", item_price.replace(" ", ""))


print(f"item_price: '{item_price}'")
print(f"parsed_price: '{parsed_price}'")
