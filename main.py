from blockchain import Blockchain
from car_sharing import Owner, Car, Customer

def show_rental_cost(cost):
    print("Rental cost: ", cost)

def start():
    blockchain = Blockchain()
    owners = {}
    customers = {}

    while True:
        print("\n1. Create Owner")
        print("2. Create Customer")
        print("3. Show Balance")
        print("4. Deploy Blockchain")
        print("5. Add Car to Rent")
        print("6. Request Booking")
        print("7. Encrypt and Store Details")
        print("8. Allow Car Usage")
        print("9. Access Car")
        print("10. End Car Rental and Show Rental Cost")
        print("11. Withdraw Earnings")
        print("12. Retrieve Balance")
        print("13. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            owner_id = input("Enter Owner ID: ")
            owners[owner_id] = Owner()
            print(f"OwnerID: {owner_id}, Balance: {owners[owner_id].balance}")

        elif choice == '2':
            customer_id = input("Enter Customer ID: ")
            customers[customer_id] = Customer()
            print(f"CustomerID: {customer_id}, Balance: {customers[customer_id].balance}")

        elif choice == '3':
            if len(owners) == 0 and len(customers) == 0:
                print("No members exist!!")
                continue
            ck_id = input("Enter ID: ")
            if ck_id in owners:
                print(f"Owner balance: {owners[ck_id].balance}")
            elif ck_id in customers:
                print(f"Owner balance: {customers[ck_id].balance}")
            else:
                print("No such ID exists.")

        elif choice == '4':
            owner_id = input("Enter Owner ID: ")
            if owner_id in owners:
                owners[owner_id].deploy(blockchain)
            else:
                print("Only owners can deploy blockchain")
            
        elif choice == '5':
            owner_id = input("Enter Owner ID: ")
            if owner_id in owners:
                owners[owner_id].add_car_to_rent()
            else:
                print("Only owners can add cars")

        elif choice == '6':
            customer_id = input("Enter Customer ID: ")
            if customer_id in customers:
                available_cars = []
                for owner_id, owner in owners.items():
                    for car_id, car_info in owner.cars.items():
                        if car_info['booking_details'] is None:
                            available_cars.append((owner_id, car_id, car_info['car']))

                if not available_cars:
                    print("No available cars.")
                else:
                    print("Available Cars:")
                    for i, (owner_id, car_id, car) in enumerate(available_cars, start=1):
                        print(f"{i}) Owner: {owner_id}, Car Name: {car.car_info}, Price: {car.day_price}")

                while True:
                    choice = int(input("Enter choice: ")) - 1
                    if 0 <= choice < len(available_cars):
                        owner_id, car_id, car = available_cars[choice]
                        customers[customer_id].request_book(blockchain)
                        customers[customer_id].pass_number_of_days()
                        owners[owner_id].allow_car_usage(car_id)
                    else:
                        user_input = input("Invalid Input!!\n**Press Enter to try again**")
                        if user_input:
                            break
            else:
                print("Only customers can rent cars")

        elif choice == '7':
            owner_id = input("Enter Owner ID: ")
            owners[owner_id].encrypt_and_store_details(blockchain)

        elif choice == '8':
            owner_id = input("Enter Owner ID: ")
            if owner_id in owners:
                owners[owner_id].allow_car_usage()
            else:
                print("Owner not found.")

        elif choice == '9':
            customer_id = input("Enter Customer ID: ")
            if customer_id in customers:
                owner_id = input("Enter Owner ID: ")
                if owner_id in owners:
                    customers[customer_id].access_car(owners[owner_id])
                else:
                    print("Owner not found.")
            else:
                print("Customer not found.")
            customers[customer_id].access_car()

        elif choice == '10':
            customer_id = input("Enter Customer ID: ")
            if customer_id in customers:
                owner_id = input("Enter Owner ID: ")
                if owner_id in owners:
                    customers[customer_id].end_car_rental(owners[owner_id])
                else:
                    print("Owner not found.")
            else:
                print("Customer not found.")

        elif choice == '11':
            owner_id = input("Enter Owner ID: ")
            owners[owner_id].withdraw_earnings()
        elif choice == '12':
            customer_id = input("Enter Customer ID: ")
            customers[customer_id].retrieve_balance()
        elif choice == '13':
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == '__main__':
    start()
