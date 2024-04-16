## Credit Card Validator

This Python script implements a basic credit card number validation using the Luhn algorithm. It prompts the user to enter the first 15 digits of a credit card number and then calculates the correct last digit based on the Luhn checksum.

### Luhn Algorithm Overview

The Luhn algorithm (also known as the mod-10 algorithm) is a checksum formula used to validate a variety of identification numbers, including credit card numbers. It works by performing the following steps:

1. **Starting from the rightmost digit (excluding the check digit)**, double the value of every second digit. If doubling results in a number greater than 9, subtract 9 from the product.
   
2. **Sum all the digits** of the modified numbers obtained in step 1, along with the untouched digits from the original number.
   
3. **Calculate the check digit** that makes the total sum a multiple of 10. This is done by taking the total sum modulo 10, and then subtracting this value from 10.

### How It Works

The script implements the Luhn algorithm with the following steps:

1. **Separating Digits**: The `separateNums(card_input)` function separates the digits of the card input into two lists:
   - `oddDoubledNumbers`: Contains modified (doubled and summed if necessary) odd-indexed digits.
   - `evenNumbers`: Contains even-indexed digits.
   
2. **Doubling and Summing**: In `separateNums(card_input)`, odd-indexed digits are doubled, and if the result is greater than 9, the sum of the resulting digits is used.
   
3. **Checksum Calculation**: The `calculateLastDigit(oddDoubledNumbers, evenNumbers)` function calculates the last digit of the credit card number using the Luhn checksum formula:
   - It sums up all the digits from `oddDoubledNumbers` and `evenNumbers`.
   - Then, it calculates the check digit (`last_digit`) that makes the total sum a multiple of 10.

4. **Validation**: The script prompts the user to input the first 15 digits of a credit card number. If the input is valid (exactly 15 digits), it proceeds with the validation process. Otherwise, it prompts the user to provide a valid input.

### Usage

1. **Input Prompt**: Run the script and enter the first 15 digits of your credit card number when prompted.

2. **Output**: The script will display the last correct digit of the credit card number based on the Luhn algorithm, as well as the full credit card number with the correct last digit appended.

### Usage Example

```bash
$ python credit_card_validator.py
Enter the first 15 digits of your card number: 123456789012345
You've entered: 123456789012345
The last correct digit of the credit card is: 5
The full credit card number with the last correct digit is: 1234567890123455
```

### Requirements

- Python 3.x (Tested on Python 3.7)

### Notes

- This script is a basic implementation of the Luhn algorithm for educational purposes and should not be used for actual credit card validation or processing.
- Always handle credit card information securely and adhere to relevant security and compliance standards when working with sensitive data.

Please refer to the script for more details on the implementation. For questions or issues, feel free to reach out or submit a pull request.
