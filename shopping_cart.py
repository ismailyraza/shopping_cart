def apply_discounts(cart, discounts):
    applicable_discounts = []
    
    if cart["subtotal"] > 200:
        applicable_discounts.append(("flat_10_discount", 10))
    
    for product in cart["products"]:
        product_price = prices[product["name"]]  # Get the price from the prices dictionary
        if product["quantity"] > 10:
            product_discount = product_price * 0.05
            applicable_discounts.append(("bulk_5_discount", product_discount))
        if cart["total_quantity"] > 20:
            cart_discount = cart["subtotal"] * 0.10
            applicable_discounts.append(("bulk_10_discount", cart_discount))
    
    if cart["total_quantity"] > 30:
        for product in cart["products"]:
            if product["quantity"] > 15:
                product_discount = prices[product["name"]] * 0.50
                applicable_discounts.append(("tiered_50_discount", product_discount))
    
    best_discount = max(applicable_discounts, key=lambda x: x[1], default=None)
    if best_discount:
        cart["discount_name"], cart["discount_amount"] = best_discount


def calculate_total(cart):
    cart["subtotal"] = sum(product["total"] for product in cart["products"])
    cart["shipping_fee"] = (cart["total_quantity"] // 10) * 5  # $5 for each package of 10 units
    cart["total"] = cart["subtotal"] - cart["discount_amount"] + cart["shipping_fee"] + cart["gift_wrap_fee"]


def main():
    cart = {
        "products": [],
        "subtotal": 0,
        "discount_name": None,
        "discount_amount": 0,
        "shipping_fee": 0,
        "gift_wrap_fee": 0,
        "total_quantity": 0
    }

    product_names = ["Product A", "Product B", "Product C"]

    for name in product_names:
        quantity = int(input(f"Enter the quantity of {name}: "))
        is_gift_wrapped = input(f"Is {name} wrapped as a gift? (yes/no): ").lower() == "yes"

        total_amount = quantity * prices[name]
        gift_wrap_fee = quantity if is_gift_wrapped else 0

        cart["products"].append({
            "name": name,
            "quantity": quantity,
            "total": total_amount,
            "gift_wrap_fee": gift_wrap_fee
        })

        cart["total_quantity"] += quantity

    apply_discounts(cart, discounts)
    calculate_total(cart)

    print("\nProduct Details:")
    for product in cart["products"]:
        print(f"{product['name']} - Quantity: {product['quantity']} - Total: ${product['total']}")
    print(f"\nSubtotal: ${cart['subtotal']}")
    print(f"Discount Applied: {cart['discount_name']} - Amount: ${cart['discount_amount']}")
    print(f"Shipping Fee: ${cart['shipping_fee']}")
    print(f"Gift Wrap Fee: ${cart['gift_wrap_fee']}")
    print(f"\nTotal: ${cart['total']}")

if __name__ == "__main__":
    prices = {"Product A": 20, "Product B": 40, "Product C": 50}
    discounts = ["flat_10_discount", "bulk_5_discount", "bulk_10_discount", "tiered_50_discount"]
    main()
