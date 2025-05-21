def count_even_numbers():
    """
    Function to take 10 integer inputs and count how many even numbers are there.
    Returns the count of even numbers.
    """
    even_count = 0
    numbers = []
    
    print("Please enter 10 integers:")
    
    # Take 10 integer inputs
    for i in range(10):
        while True:
            try:
                num = int(input(f"Enter number {i+1}: "))
                numbers.append(num)
                if num % 2 == 0:
                    even_count += 1
                break
            except ValueError:
                print("Invalid input! Please enter an integer.")
    
    # Print the results
    print("\nResults:")
    print(f"Numbers entered: {numbers}")
    print(f"Number of even numbers: {even_count}")
    
    return even_count

if __name__ == "__main__":
    try:
        count = count_even_numbers()
        print(f"\nThere are {count} even numbers in the input.")
    except Exception as e:
        print(f"An error occurred: {str(e)}") 