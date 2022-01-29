from server.utils import start_server, create_parser

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    start_server(args.address, args.port, args.size)
