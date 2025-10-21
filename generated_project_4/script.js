// script.js

// Function to add two numbers
function add(a, b) {
    if (isNaN(a) || isNaN(b)) {
        return 'Invalid input';
    }
    return a + b;
}

// Function to subtract two numbers
function subtract(a, b) {
    if (isNaN(a) || isNaN(b)) {
        return 'Invalid input';
    }
    return a - b;
}

// Function to multiply two numbers
function multiply(a, b) {
    if (isNaN(a) || isNaN(b)) {
        return 'Invalid input';
    }
    return a * b;
}

// Function to divide two numbers
function divide(a, b) {
    if (isNaN(a) || isNaN(b)) {
        return 'Invalid input';
    }
    if (b === 0) {
        return 'Cannot divide by zero';
    }
    return a / b;
}

// Function to initialize the calculator
function initCalculator() {
    const display = document.getElementById('display');
    let currentInput = '';
    let firstOperand = null;
    let operator = null;

    const buttons = document.querySelectorAll('.buttons button');
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const buttonValue = button.innerText;
            if (!isNaN(buttonValue)) {
                currentInput += buttonValue;
                display.value = currentInput;
            } else if (['+', '-', '*', '/'].includes(buttonValue)) {
                if (currentInput) {
                    firstOperand = parseFloat(currentInput);
                    operator = buttonValue;
                    currentInput = '';
                }
            } else if (buttonValue === '=') {
                if (firstOperand !== null && operator && currentInput) {
                    const secondOperand = parseFloat(currentInput);
                    let result;
                    switch (operator) {
                        case '+':
                            result = add(firstOperand, secondOperand);
                            break;
                        case '-':
                            result = subtract(firstOperand, secondOperand);
                            break;
                        case '*':
                            result = multiply(firstOperand, secondOperand);
                            break;
                        case '/':
                            result = divide(firstOperand, secondOperand);
                            break;
                    }
                    display.value = result;
                    currentInput = '';
                    firstOperand = null;
                    operator = null;
                }
            }
        });
    });
}

// Call initCalculator when DOM is fully loaded
document.addEventListener('DOMContentLoaded', initCalculator);