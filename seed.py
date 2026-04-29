from decimal import Decimal
from app.component.database.database import get_db
from app.component.category.category import Category
from app.component.product.product import Product


#Seed the database with some initial data
def seed():
    db = next(get_db())

    groceries = Category(name="Groceries")
    db.add(groceries)
    db.flush()

    fruits_veg = Category(name="Fruits & Vegetables", parent_id=groceries.id)
    meat_seafood = Category(name="Meat & Seafood", parent_id=groceries.id)
    dairy_eggs = Category(name="Dairy & Eggs", parent_id=groceries.id)
    beverages = Category(name="Beverages", parent_id=groceries.id)
    pantry_household = Category(name="Pantry & Household", parent_id=groceries.id)

    db.add_all([fruits_veg, meat_seafood, dairy_eggs, beverages, pantry_household])
    db.flush()

    fruits = Category(name="Fruits", parent_id=fruits_veg.id)
    vegetables = Category(name="Vegetables", parent_id=fruits_veg.id)
    meat = Category(name="Meat", parent_id=meat_seafood.id)
    seafood = Category(name="Seafood", parent_id=meat_seafood.id)

    db.add_all([fruits, vegetables, meat, seafood])
    db.flush()

    products = [
        Product(sku="GRO-BRD-APP-016", title="Apple", description="Fresh and crisp apples, perfect for snacking or incorporating into various recipes.", image="https://cdn.dummyjson.com/product-images/groceries/apple/thumbnail.webp", price=Decimal("1.99"), category_id=fruits.id),
        Product(sku="GRO-BRD-KIW-030", title="Kiwi", description="Nutrient-rich kiwi, perfect for snacking or adding a tropical twist to your dishes.", image="https://cdn.dummyjson.com/product-images/groceries/kiwi/thumbnail.webp", price=Decimal("2.49"), category_id=fruits.id),
        Product(sku="GRO-BRD-LEM-031", title="Lemon", description="Zesty and tangy lemons, versatile for cooking, baking, or making refreshing beverages.", image="https://cdn.dummyjson.com/product-images/groceries/lemon/thumbnail.webp", price=Decimal("0.79"), category_id=fruits.id),
        Product(sku="GRO-BRD-MUL-033", title="Mulberry", description="Sweet and juicy mulberries, perfect for snacking or adding to desserts and cereals.", image="https://cdn.dummyjson.com/product-images/groceries/mulberry/thumbnail.webp", price=Decimal("4.99"), category_id=fruits.id),
        Product(sku="GRO-BRD-STR-040", title="Strawberry", description="Sweet and succulent strawberries, great for snacking, desserts, or blending into smoothies.", image="https://cdn.dummyjson.com/product-images/groceries/strawberry/thumbnail.webp", price=Decimal("3.99"), category_id=fruits.id),

        Product(sku="GRO-BRD-CUC-021", title="Cucumber", description="Crisp and hydrating cucumbers, ideal for salads, snacks, or as a refreshing side.", image="https://cdn.dummyjson.com/product-images/groceries/cucumber/thumbnail.webp", price=Decimal("1.49"), category_id=vegetables.id),
        Product(sku="GRO-BRD-GRE-025", title="Green Bell Pepper", description="Fresh and vibrant green bell pepper, perfect for adding color and flavor to your dishes.", image="https://cdn.dummyjson.com/product-images/groceries/green-bell-pepper/thumbnail.webp", price=Decimal("1.29"), category_id=vegetables.id),
        Product(sku="GRO-BRD-GRE-026", title="Green Chili Pepper", description="Spicy green chili pepper, ideal for adding heat to your favorite recipes.", image="https://cdn.dummyjson.com/product-images/groceries/green-chili-pepper/thumbnail.webp", price=Decimal("0.99"), category_id=vegetables.id),
        Product(sku="GRO-BRD-POT-035", title="Potatoes", description="Versatile and starchy potatoes, great for roasting, mashing, or as a side dish.", image="https://cdn.dummyjson.com/product-images/groceries/potatoes/thumbnail.webp", price=Decimal("2.29"), category_id=vegetables.id),
        Product(sku="GRO-BRD-ONI-037", title="Red Onions", description="Flavorful and aromatic red onions, perfect for adding depth to your savory dishes.", image="https://cdn.dummyjson.com/product-images/groceries/red-onions/thumbnail.webp", price=Decimal("1.99"), category_id=vegetables.id),

        Product(sku="GRO-BRD-BEE-017", title="Beef Steak", description="High-quality beef steak, great for grilling or cooking to your preferred level of doneness.", image="https://cdn.dummyjson.com/product-images/groceries/beef-steak/thumbnail.webp", price=Decimal("12.99"), category_id=meat.id),
        Product(sku="GRO-BRD-CHI-019", title="Chicken Meat", description="Fresh and tender chicken meat, suitable for various culinary preparations.", image="https://cdn.dummyjson.com/product-images/groceries/chicken-meat/thumbnail.webp", price=Decimal("9.99"), category_id=meat.id),

        Product(sku="GRO-BRD-FIS-024", title="Fish Steak", description="Quality fish steak, suitable for grilling, baking, or pan-searing.", image="https://cdn.dummyjson.com/product-images/groceries/fish-steak/thumbnail.webp", price=Decimal("14.99"), category_id=seafood.id),

        Product(sku="GRO-BRD-MIL-032", title="Milk", description="Fresh and nutritious milk, a staple for various recipes and daily consumption.", image="https://cdn.dummyjson.com/product-images/groceries/milk/thumbnail.webp", price=Decimal("3.49"), category_id=dairy_eggs.id),
        Product(sku="GRO-BRD-EGG-023", title="Eggs", description="Fresh eggs, a versatile ingredient for baking, cooking, or breakfast.", image="https://cdn.dummyjson.com/product-images/groceries/eggs/thumbnail.webp", price=Decimal("2.99"), category_id=dairy_eggs.id),
        Product(sku="GRO-BRD-CRE-028", title="Ice Cream", description="Creamy and delicious ice cream, available in various flavors for a delightful treat.", image="https://cdn.dummyjson.com/product-images/groceries/ice-cream/thumbnail.webp", price=Decimal("5.49"), category_id=dairy_eggs.id),

        Product(sku="GRO-BRD-JUI-029", title="Juice", description="Refreshing fruit juice, packed with vitamins and great for staying hydrated.", image="https://cdn.dummyjson.com/product-images/groceries/juice/thumbnail.webp", price=Decimal("3.99"), category_id=beverages.id),
        Product(sku="GRO-BRD-NES-034", title="Nescafe Coffee", description="Quality coffee from Nescafe, available in various blends for a rich and satisfying cup.", image="https://cdn.dummyjson.com/product-images/groceries/nescafe-coffee/thumbnail.webp", price=Decimal("7.99"), category_id=beverages.id),
        Product(sku="GRO-BRD-SOF-039", title="Soft Drinks", description="Assorted soft drinks in various flavors, perfect for refreshing beverages.", image="https://cdn.dummyjson.com/product-images/groceries/soft-drinks/thumbnail.webp", price=Decimal("1.99"), category_id=beverages.id),
        Product(sku="GRO-BRD-WAT-042", title="Water", description="Pure and refreshing bottled water, essential for staying hydrated throughout the day.", image="https://cdn.dummyjson.com/product-images/groceries/water/thumbnail.webp", price=Decimal("0.99"), category_id=beverages.id),

        Product(sku="GRO-BRD-COO-020", title="Cooking Oil", description="Versatile cooking oil suitable for frying, sautéing, and various culinary applications.", image="https://cdn.dummyjson.com/product-images/groceries/cooking-oil/thumbnail.webp", price=Decimal("4.99"), category_id=pantry_household.id),
        Product(sku="GRO-BRD-HON-027", title="Honey Jar", description="Pure and natural honey in a convenient jar, perfect for sweetening beverages or drizzling over food.", image="https://cdn.dummyjson.com/product-images/groceries/honey-jar/thumbnail.webp", price=Decimal("6.99"), category_id=pantry_household.id),
        Product(sku="GRO-BRD-RIC-038", title="Rice", description="High-quality rice, a staple for various cuisines and a versatile base for many dishes.", image="https://cdn.dummyjson.com/product-images/groceries/rice/thumbnail.webp", price=Decimal("5.99"), category_id=pantry_household.id),
        Product(sku="GRO-BRD-PRO-036", title="Protein Powder", description="Nutrient-packed protein powder, ideal for supplementing your diet with essential proteins.", image="https://cdn.dummyjson.com/product-images/groceries/protein-powder/thumbnail.webp", price=Decimal("19.99"), category_id=pantry_household.id),
        Product(sku="GRO-BRD-FOO-018", title="Cat Food", description="Nutritious cat food formulated to meet the dietary needs of your feline friend.", image="https://cdn.dummyjson.com/product-images/groceries/cat-food/thumbnail.webp", price=Decimal("8.99"), category_id=pantry_household.id),
        Product(sku="GRO-BRD-FOO-022", title="Dog Food", description="Specially formulated dog food designed to provide essential nutrients for your canine companion.", image="https://cdn.dummyjson.com/product-images/groceries/dog-food/thumbnail.webp", price=Decimal("10.99"), category_id=pantry_household.id),
        Product(sku="GRO-BRD-TIS-041", title="Tissue Paper Box", description="Convenient tissue paper box for everyday use, providing soft and absorbent tissues.", image="https://cdn.dummyjson.com/product-images/groceries/tissue-paper-box/thumbnail.webp", price=Decimal("2.49"), category_id=pantry_household.id),
    ]

    db.add_all(products)
    db.commit()
    print(f"Seeded: 1 parent category, 5 sub-categories, 4 sub-sub-categories, {len(products)} products.")


if __name__ == "__main__":
    seed()
