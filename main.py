import sys


def argumentation(BASE_URL):
    args = BASE_URL
    if len(args) < 2:
        print("no website provided")
        return sys.exit(1),
    if len(args) > 2:
        print("too many arguments provided")
        return sys.exit(1)
    if len(args) == 2:
        url = sys.argv[1]
        return f"starting crawl of: {url}"
def main():
    print(argumentation(sys.argv))


if __name__ == "__main__":
    main()
