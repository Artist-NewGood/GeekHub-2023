from modules.order_robot import OrderRobotSpareBinIndustries
from modules.read_order_file import OrderRead


ORDER_FILE_LINK = 'https://robotsparebinindustries.com/orders.csv'


def main() -> None:
    """The main function to fulfill robot orders. Uses the OrderRobotSpareBin class to automate the order
       fulfillment process. Reads data from the CSV file, provided by ORDER_FILE_LINK link, and for each
       line it executes the order with the corresponding parameters."""

    with OrderRobotSpareBinIndustries() as order_robot:
        order_robot.open_order_page()
        order_robot.output_folder()

        for _, head, body, legs, address in OrderRead(link=ORDER_FILE_LINK).read_order_file():
            order_robot.order_part(head, body, legs, address)


if __name__ == '__main__':
    main()
