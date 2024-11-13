class Client:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def authenticate(self, password):
        return self.password == password

class Item:
    def __init__(self, item_id, name, category, price, stock_quantity):
        self.item_id = item_id
        self.name = name
        self.category = category
        self.price = price
        self.stock_quantity = stock_quantity

    def update_stock(self, quantity):
        self.stock_quantity += quantity

    def __str__(self):
        return f"{self.item_id}: {self.name}: | Category: {self.category} | Price: ${self.price} | {self.stock_quantity}"
    
class Inventory:
    def __init__(self):
        self.items = {} # dictionary 
        self.low_stock_threshold = 5 # instance variable

    def add_item(self, item):
        if item.item_id in self.items:
            print("Error: Item ID Already Exists.")
        else:
            self.items[item.item_id] = item
            print("Item added Successfully.")

    def edit_item(self, item_id, **kwargs):
        print("item_id", item_id)
        print(self.items)  
        item = self.items.get(item_id)
        if not item:
            print("Error, Item not found.")
            return

        for key, value in kwargs.items():
            setattr(item, key, value)
        print(" Item Updates Successfully.")

    def delete_item(self, item_id):
        if item_id in self.items:
            del self.items[item_id]
            print("item deleted successfully.")
        else:
            print("item not found.")

    def view_items(self):
        if not self.items:
            print("No items in inventory.") 
        for item in self.items.values():
            print(item)
            if item.stock_quantity < self.low_stock_threshold:
                print(f"Warning: {item.name} stock is low!")

    def search_item(self, name=None, category=None):
        results = []
        for item in self.items.values():
            if name and name.lower() in item.name.lower():
                results.append(item)
            elif category and category.lower() == item.category.lower():
                results.append(item)

        if results:
            for item in results:
                print(item)
        else:
            print("No items found")

    def adjust_stock(self, item_id, quantity):
        item = self.items.get(item_id)
        if not item:
            print("Error: Item not found.")
            return
        
        item.update_stock(quantity)
        print("Stock updated successfully.")

class InventorySystem:
    def __init__(self):
        self.inventory = Inventory()
        self.clients = {
            "admin": Client("admin", "admin123", "Admin"),
            "user": Client("user", "user123", "User")
        }
        self.current_client = None

    def login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        client = self.clients.get(username)

        if client and client.authenticate(password):
           self.current_client = client
           print(f"Welcome, {client.username} ({client.role})!")
           return True
        else:
            print("Invalid Login")
            return True
        
    def run(self):
        if not self.login():
            return

        while True:
            if self.current_client.role == "Admin":
                print("\nOptions: 1. Add Item 2. Edit Item 3. Delete Item 4. View Items 5. Adjust Stock 6. Search Item 7. Logout")
            else:
                print("\nOptions: 1. View Items 2. Search Item 3. Logout")

            choice = input("Enter your choice:")

            if choice == "1":
                if self.current_client.role == "Admin":
                    self.add_item()
                else:
                    self.inventory.view_items()

            elif choice == "2":
                if self.current_client.role == "Admin":
                    self.edit_item()
                else:
                    self.search_item()

            elif choice == "3":
                if self.current_client.role == "Admin":
                    self.delete_item()
                else:
                    break

            elif choice == "4" and self.current_client.role == "Admin":
                self.inventory.view_items()  

            elif choice == "5" and self.current_client.role == "Admin":
                self.adjust_stock()

            elif choice == "6" and self.current_client.role == "Admin":
                self.search_item()

            elif choice == "7" and self.current_client.role == "Admin":
                break 

            else:
                print("Invalid choice, please try again.")  



    def add_item(self):
        item_id = input("Enter item ID: ")                    
        name = input("Enter item name: ")                    
        category = input("Enter item category: ")                    
        price = float(input("Enter item price: "))                    
        stock_quantity = int(input("Enter stock quantity: "))                    
        item = Item(item_id, name, category, price, stock_quantity)
        self.inventory.add_item(item) 

    def edit_item(self):
        item_id = input("Enter item ID to edit: ")
        name = input("Enter new name (leave blank to skip): ")
        category = input("Enter new category (leave blank to skip): ")
        price = input("Enter new price (leave blank to skip): ")
        stock_quantity = input("Enter new stock quantity (leave blank to skip): ")                       
                        
        kwargs = {}

        if name:
            kwargs["name"] = name
        if category:
            kwargs["category"] = category    
        if price:
            kwargs["price"] = float(price)    
        if stock_quantity:
            kwargs["stock_quantity"] = int(stock_quantity)
        print(kwargs)

        self.inventory.edit_item(item_id, **kwargs)
    
    def delete_item(self):
        item_id = input("Enter item ID to delete: ")
        self.inventory.delete_item(item_id)
    
    def adjust_stock(self):
        item_id = input("Enter item ID to adjust stock: ")
        quantity = int(input("Enter quantity to ajust (positive to restock, nega3tive to reduce): "))
        self.inventory.adjust_stock(item_id, quantity)
    
    def search_item(self):
        name = input("Enter item name to search (leave blank for category): ")
        category = input("Enter category: ")
        self.inventory.search_item(name=name, category=category)

        
if __name__ == "__main__":
    system = InventorySystem()
    system.run()   





