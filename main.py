import sys


def argumentation(BASE_URL):
    args = BASE_URL
    if len(args) < 2:
        print("no website provided")
        sys.exit(1),
    if len(args) > 2:
        print("too many arguments provided")
        sys.exit(1)
    return sys.argv[1]
def main():
    url = argumentation(sys.argv)
    print(f"starting crawl of: {url}")

if __name__ == "__main__":
    main()
