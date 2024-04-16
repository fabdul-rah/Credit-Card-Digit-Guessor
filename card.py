def separateNums(card_input):
    oddDoubledNumbers = []
    evenNumbers = []

    for i, char in enumerate(card_input):
        if i % 2 == 0:
            doubled_value = int(char) * 2
            if doubled_value > 9:
                sum_of_digits = (doubled_value // 10) + (doubled_value % 10)
                oddDoubledNumbers.append(sum_of_digits)
            else:
                oddDoubledNumbers.append(doubled_value)
        else:
            evenNumbers.append(int(char))
    return oddDoubledNumbers, evenNumbers

def calculateLastDigit(oddDoubledNumbers, evenNumbers):
    total_sum = sum(oddDoubledNumbers) + sum(evenNumbers)
    last_digit = (10 - (total_sum % 10)) % 10  # Luhn Algorithm
    return last_digit

card_input = input("Enter the first 15 digits of your card number: ")

if card_input.isdigit() and len(card_input) == 15:
    print("You've entered:", card_input)
    oddDoubledNumbers, evenNumbers = separateNums(card_input)
    
    last_digit = calculateLastDigit(oddDoubledNumbers, evenNumbers)
    full_credit_card_number = card_input + str(last_digit)
    
    print("The last correct digit of the credit card is:", last_digit)
    print("The full credit card number with the last correct digit is:", full_credit_card_number)
    
else:
    print("Input must be exactly 15 digits!")