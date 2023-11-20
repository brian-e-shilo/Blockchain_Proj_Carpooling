from contract import SmartContract, BookingDetails

class Owner:
    def __init__(self):
        self.contract = SmartContract()
        self.balance = float(input("Enter initial balance for Owner: "))
        self.cars = {}
        self.pending_requests = []

    def add_car_to_rent(self):
        car_info = input("Enter the car you want to add: ")
        day_price = float(input("Enter the daily rental price for the car: "))
        while True:
            car_id = input("Enter a unique ID for the car: ")
            if car_id in self.cars:
                print("Car with the same ID already exists. Please choose a different ID.")
                continue
            break

        new_car = Car(car_info, day_price)
        self.cars[car_id] = {
            'car': new_car,
            'day_price': day_price,
            'booking_details': None
        }
        print(f"Added  {car_info}: {day_price}")

        self.contract.add_booking_details(BookingDetails(new_car, day_price))

    def deploy(self, blockchain):
        while True:
            eth = float(input("Enter the amount of Ether to deploy: "))
            if self.balance-eth <=0:
                user_input = input("Insufficient Balance!!\n**Press Enter to try again**")
                if user_input:
                    break
                continue
            self.balance -= eth
            self.contract.owner_deposit(eth)
            blockchain.add_new_transaction(self.contract)
            print(f"{eth} Ether deployed")

    def withdraw_earnings(self):
        self.balance += self.contract.withdraw_earnings()

    def view_pending_requests(self):
        if not self.pending_requests:
            print("No pending requests.")
        else:
            print("Pending Requests:")
            for index, request in enumerate(self.pending_requests, start=1):
                print(f"{index}. Car: {request['car_info']}, Customer ID: {request['customer_id']}")

    def allow_car_usage(self):
        self.view_pending_requests()  # Display pending requests to the owner
        if not self.pending_requests:
            print("No pending requests to approve.")
            return

        choice = input("Enter the number of the request to approve (0 to cancel): ")
        if choice == '0':
            print("Approval canceled.")
            return

        try:
            choice = int(choice)
            if 1 <= choice <= len(self.pending_requests):
                request = self.pending_requests.pop(choice - 1)
                # Now you can proceed with allowing car usage for the selected request
                self.contract.allow_car_usage()
                print(f"Approved request for Car: {request['car_info']} for Customer ID: {request['customer_id']}")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def encrypt_and_store_details(self, blockchain):
        blockchain.mine()

class Customer:
    def __init__(self):
        self.contract = SmartContract()
        self.balance = float(input("Enter initial balance for Customer: "))

    def request_book(self, blockchain):
        eth = float(input("Enter the amount of Ether for booking: "))
        self.contract = blockchain.get_unconfirmed_transactions()[0]
        self.contract.client_deposit(eth)
        self.balance -= eth

    def pass_number_of_days(self):
        days_no = int(input("Enter the number of days for rental: "))
        booking_details = self.contract.get_booking_details()
        booking_details.request(days_no)

    def retrieve_balance(self):
        self.balance += self.contract.retrieve_balance()

    def access_car(self, owner):
        if owner.contract.is_car_allowed():
            self.contract.get_car().access()
        else:
            print("Access denied. Car access needs approval from the owner.")


class Car:
    def __init__(self, car_info, day_price):
        self.car_info = car_info
        self.day_price = day_price
        self.is_rented = False
        self.allowed_to_use = False

    def access(self):
        print("Car has been accessed")
        self.is_rented = True

    def end_rental(self):
        self.is_rented = False

    def allow_to_use(self):
        self.allowed_to_use = True
