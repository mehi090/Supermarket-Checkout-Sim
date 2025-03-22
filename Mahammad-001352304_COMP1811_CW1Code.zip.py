import random
from datetime import datetime
import time


def my_function():  # Function to timestamp
    current_time = datetime.now()
    timestamp = current_time.strftime("00:00")  # Set the timestamp to 00:00
    print(timestamp)  # print timestamp


class GenerateLane:  # Class for the checkout Lane, contains most of the required functions needed for each customer
    def __init__(self, lane_type, max_customers, max_basket_size, processing_time):
        self.lane_type = lane_type  # Sets the lane type for each lane. Either Self or Regular
        self.max_customers = max_customers  # This is for lane capacity
        self.max_basket_size = max_basket_size  # This is for deciding which lane the customer will be assigned to
        self.processing_time = processing_time  # This calculated checkout out time for each customer depending on
        # basket size
        self.customers_in_lane = []  # This is a list representing the customers in lane
        self.customer_basket = []  # Customer basket size
        self.is_open = False  # Flag to indicate if the lane is open

    def add_customer(self, customer):  # Add Customer to lane
        if len(self.customers_in_lane) < self.max_customers and len(customer.shopping_basket) <= self.max_basket_size:
            self.customers_in_lane.append(customer)
            customer.lanes_visited.append(self.lane_type)  # Update the list of lanes visited
        else:
            GenerateLane.change_lane(self, customer)  # Run the change lane function

    def remove_customer(self, customer):  # Remove Customer after checkout
        if customer in self.customers_in_lane:
            self.customers_in_lane.remove(customer)  # Remove customer from the list
            print("Customer " + str(customer.customer_number) + " left " + self.lane_type + " lane after checkout.")
        else:
            print("Customer " + str(customer.customer_number) + " not found in " + self.lane_type + " lane.")

    def change_lane(self, customer):  # Change the lane for the customer if the lane is too full
        print(self.lane_type,
              "lane is full or lane line is too long. Adding Customer ", customer.customer_number,
              " to another lane...")

    def process_checkout(self, customer):  # Process the checkout for a customer
        num_items = len(customer.shopping_basket)
        processing_time = num_items * self.processing_time
        return processing_time

    def open_lane(self):  # Set a lane to open
        self.is_open = True
        print(self.lane_type + " lane is now open.")

    def close_lane(self):  # Set a lane to close
        self.is_open = False
        print(self.lane_type + " lane is now closed.")

    def generate_random_shopping_item(self):  # Generate random basket with this inventory
        inventory = ['milk', 'sugar', 'eggs', 'bread', 'oats', 'fish', 'meat', 'apples',
                     'bananas', 'orange juice', 'cheese', 'yogurt', 'chicken', 'beef', 'lettuce',
                     'tomatoes', 'potatoes', 'onions', 'pasta', 'rice', 'cookies', 'chocolate',
                     'toothpaste', 'shampoo', 'soap', 'toilet paper', 'laundry detergent', 'coffee', 'tea']
        return random.choice(inventory)  # randomize the inventory

    def generate_shopping_basket(self):
        num_items = random.randint(1, 30)  # Give each customer between 1 and 30 items
        self.customer_basket = [self.generate_random_shopping_item() for i in range(num_items)]  # Generate a basket
        # for each customer


class Customer:  # Class definition for Customer
    def __init__(self, customer_number):
        self.customer_number = customer_number
        self.lane_type = None
        self.lottery_ticket = False
        self.lottery_number = random.randint(0, 1)  # Lottery Number used to randomize lottery ticket
        self.shopping_basket = []  # List to store customer shipping basket
        self.lanes_visited = []  # List to store which lanes the customer visited

    def generate_shopping_basket(self, GenerateLane):
        GenerateLane.generate_shopping_basket()  # Call the GenerateLane class and inheritance shopping basket
        self.shopping_basket = GenerateLane.customer_basket  # Set the shopping list to the GenerateLane shopping basket
        num_items = len(self.shopping_basket)  # Set num_items to the length of the shopping basket
        if num_items <= 10:  # Set condition for the lane type to the number of items in the basket
            self.lane_type = "Self-Checkout"
        else:
            self.lane_type = "Regular Lane"

        return num_items, self.lane_type

    def lottery_ticket_result(self):  # Award a lottery ticket if the customer has at least 10 items
        num_items = len(self.shopping_basket)
        if num_items >= 10 and self.lottery_number == 1:
            print("You won a lottery ticket!")
            self.lottery_ticket = True  # Set lottery_ticket to True
        if num_items >= 10 and self.lottery_number == 0:
            print("You didn't win a lottery ticket, sorry!")
            self.lottery_ticket = False
        else:
            pass


class CheckoutProcess:  # Class definition for Checkout Process
    def __init__(self):
        self.regular_lanes = [GenerateLane(lane_type="Regular Lane " + str(i + 1), max_customers=5, max_basket_size=31,
                                           processing_time=4) for i in range(5)]
        self.self_checkout_lanes = [
            GenerateLane(lane_type="Self-Checkout Lane " + "1", max_customers=15, max_basket_size=10,
                         processing_time=6)]

        # Open one regular and one self-checkout lane initially
        self.regular_lanes[0].open_lane()
        self.self_checkout_lanes[0].open_lane()

    def assign_customer_to_lane(self, customer):  # Assign customers to Self Checkout if they less than 10 items
        if len(customer.shopping_basket) <= 10:
            for lane in self.self_checkout_lanes:
                if lane.is_open:
                    lane.add_customer(customer)
                    if len(lane.customers_in_lane) < lane.max_customers:
                        return

        else:
            if len(customer.shopping_basket) > 10:  # Assign customer to the Regular lane if they have more than 10
                for lane in self.regular_lanes:
                    if lane.is_open:
                        # Check if the current lane is full --> THIS IS CHATGPT
                        if len(lane.customers_in_lane) < lane.max_customers:
                            lane.add_customer(customer)
                            return
                        else:
                            # Find the next available open lane
                            for next_lane in self.regular_lanes:
                                if len(next_lane.customers_in_lane) < next_lane.max_customers:
                                    next_lane.add_customer(customer)
                                    return

    def checkout_customer(self, customer):
        checkout_time_cashier = 4 * len(customer.shopping_basket)  # 4 seconds per item at cashier
        checkout_time_self_service = 6 * len(customer.shopping_basket)  # 6 seconds per item at self-service

        print("\n### Checkout for Customer " + str(customer.customer_number))
        time.sleep(.25)
        print("Customer " + str(customer.customer_number) + " added to ", customer.lane_type, "lane.")
        time.sleep(.25)
        print("Items in Basket: " + str(len(customer.shopping_basket)))
        time.sleep(.25)

        customer.lottery_ticket_result()
        time.sleep(.25)

        print("Time to process basket at cashier till:", checkout_time_cashier, " secs")
        time.sleep(.5)
        print("Time to process basket at self-service till: ", checkout_time_self_service, " secs")
        time.sleep(.5)

        # Remove customer from the lane after checkout
        if customer.lane_type == "Regular Lane":
            for lane in self.regular_lanes:
                if customer in lane.customers_in_lane:
                    lane.remove_customer(customer)
                    time.sleep(.5)
        else:
            for lane in self.self_checkout_lanes:
                if customer in lane.customers_in_lane:
                    lane.remove_customer(customer)
                    time.sleep(.5)

    def display_lane_status(self, customers_in_lane):  # Display lane status at the beginning of the simulation
        print("\n### Lane status at the start of simulation ###")
        print("Total number of customers waiting to check out at 00:00 is: ", len(customers_in_lane))

        for lane in self.regular_lanes + self.self_checkout_lanes:  # Showcase the star for each customer in lane
            if len(lane.customers_in_lane) != 0:
                print(lane.lane_type + "-> " + str(('* ' * len(lane.customers_in_lane))))
            else:
                print(lane.lane_type + "-> Closed")  # If no customer is the list lane, close lane

    def display_lane_status_updated(self, customers_in_lane):
        print("\n### Lane status at the end of the simulation ###")
        print("Total number of customers waiting to check out after 00:30 is: ", 0)

        for lane in self.regular_lanes + self.self_checkout_lanes:
            if len(lane.customers_in_lane) != 0:
                print(lane.lane_type + "-> " + str(('* ' * len(lane.customers_in_lane))))
            else:
                print(lane.lane_type + "-> Closed")


def initiate_simulation():  # Initiate the simulation

    # Record the timestamp
    my_function()

    # Initialize Checkout Process
    checkout_process = CheckoutProcess()

    # Simulate customers
    customers_in_lane = []
    for i in range(random.randint(1, 10)):
        customer = Customer(customer_number=len(customers_in_lane) + 1)
        num_type = customer.generate_shopping_basket(
            random.choice(checkout_process.regular_lanes + checkout_process.self_checkout_lanes))
        checkout_process.assign_customer_to_lane(customer)
        customers_in_lane.append(customer)

    # Display initial lane status
    checkout_process.display_lane_status(customers_in_lane)

    for customer in customers_in_lane:  # Checkout customers
        checkout_process.checkout_customer(customer)

    checkout_process.display_lane_status_updated(customers_in_lane)  # Display final lane status


def continue_simulation():  # Continue the simulation

    # Record the timestamp
    my_function()

    # Initialize Checkout Process
    checkout_process = CheckoutProcess()

    # Simulate customers
    customers_in_lane = []
    for i in range(random.randint(1, 40)):
        customer = Customer(customer_number=len(customers_in_lane) + 1)
        num_items = customer.generate_shopping_basket(
            random.choice(checkout_process.regular_lanes + checkout_process.self_checkout_lanes))
        checkout_process.assign_customer_to_lane(customer)
        customers_in_lane.append(customer)

    # Display initial lane status
    checkout_process.display_lane_status(customers_in_lane)

    for customer in customers_in_lane:  # Checkout customers
        checkout_process.checkout_customer(customer)

    checkout_process.display_lane_status_updated(customers_in_lane)  # Display final lane status


initiate_simulation()  # Call the initiate_simulation function
time.sleep(1)  # Wait for 1 second

while True:  # Continue running the second part of the simulation indefinitely
    continue_simulation()
