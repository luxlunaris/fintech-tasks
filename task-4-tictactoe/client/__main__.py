from client.utils import create_parser, connect

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    connect(args.address, args.port)
