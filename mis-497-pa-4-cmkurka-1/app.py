def rot13(text):
    # ROT-13
    result = []
    for char in text:
        if 'A' <= char <= 'Z':
            result.append(chr((ord(char) - ord('A') + 13) % 26 + ord('A')))
        elif 'a' <= char <= 'z':
            result.append(chr((ord(char) - ord('a') + 13) % 26 + ord('a')))
        else:
            result.append(char)
    return ''.join(result)


def encode_file():
    # Input the file and encode
    input_file = input("Enter the name of the file to encode: ").strip()
    try:
        with open(input_file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.\n")
        return

    encoded_content = rot13(content)

    output_file = input("Enter the name of the file to store the encoded content: ").strip()
    with open(output_file, 'w') as f:
        f.write(encoded_content)

    print(f"File encoded successfully and saved to '{output_file}'.\n")


def decode_file():
    # Input the file and decode
    input_file = input("Enter the name of the file to decode: ").strip()
    try:
        with open(input_file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.\n")
        return

    decoded_content = rot13(content)

    output_file = input("Enter the name of the file to store the decoded content: ").strip()
    with open(output_file, 'w') as f:
        f.write(decoded_content)

    print(f"File decoded successfully and saved to '{output_file}'.\n")


def word_count():
    # Input the file and word count
    input_file = input("Enter the name of the file to count words: ").strip()
    try:
        with open(input_file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.\n")
        return

    count = len(content.split())
    print(f"Total word count in '{input_file}': {count}\n")


def display_menu():
    # Menu display
    print("-" * 35)
    print("       FILE MENU SYSTEM")
    print("-" * 35)
    print("1. Encode a file")
    print("2. Decode a file")
    print("3. Word Count")
    print("4. Exit")
    print("-" * 35)


def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            encode_file()
        elif choice == '2':
            decode_file()
        elif choice == '3':
            word_count()
        elif choice == '4':
            print("Exiting the system, goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.\n")


if __name__ == "__main__":
    main()