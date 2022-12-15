import argparse



def main():
    """
    Description  message

    """

    parser = argparse.ArgumentParser(description='Calculate some operation with 2 numbers')

    parser.add_argument('operation',
                        type=str,
                        metavar="""('list', 'update'""",
                        choices=['list', 'update'],
                        help="operation ['list', 'update']")

    parser.add_argument('element',
                        type=str,
                        metavar="""('product', 'price'""",
                        choices=['product', 'price'],
                        help="update ['product', 'price']")

    parser.add_argument('req',
                        type=float,
                        metavar='enter your requirement',
                        help='enter a text to update or list specific product or price')

    parser.add_argument('-l',
                        '--l',
                        action='store_true',
                        help='prints messages')

    parser.add_argument('num_limit',
                        type=float,
                        metavar='number of items to list',
                        help='limit the quantity of items to list, insert a number')



    args = parser.parse_args()
    function_dictionary = {'operation': operation, 'element': element, 'req': req, '-l': is_limit, 'num_limit': num_limit}
    operation_value = args.operation
    element_value = args.element
    req_value = args.req
    is_limit_value = args.is_limit
    num_limit_value = args.num_limit

    if ....



if __name__ == '__main__':
    """Welcome message"""
    main()

