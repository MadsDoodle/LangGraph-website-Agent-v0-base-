class Calculator {
    add(a, b) {
        return a + b;
    }

    subtract(a, b) {
        return a - b;
    }

    multiply(a, b) {
        return a * b;
    }

    divide(a, b) {
        if (b === 0) {
            throw new Error('Cannot divide by zero');
        }
        return a / b;
    }

    calculate(operation, a, b) {
        switch (operation) {
            case 'add':
                return this.add(a, b);
            case 'subtract':
                return this.subtract(a, b);
            case 'multiply':
                return this.multiply(a, b);
            case 'divide':
                return this.divide(a, b);
            default:
                throw new Error('Invalid operation');
        }
    }
}

const calculator = new Calculator();
const resultDisplay = document.querySelector('#result-display');
const buttons = document.querySelectorAll('.digit, .operation');
let firstOperand = null;
let secondOperand = null;
let currentOperation = null;

buttons.forEach(button => {
    button.addEventListener('click', () => {
        const value = button.textContent;
        if (button.classList.contains('digit')) {
            if (currentOperation === null) {
                firstOperand = (firstOperand ? firstOperand.toString() + value : value);
                resultDisplay.textContent = firstOperand;
            } else {
                secondOperand = (secondOperand ? secondOperand.toString() + value : value);
                resultDisplay.textContent = secondOperand;
            }
        } else if (button.classList.contains('operation')) {
            currentOperation = button.id.replace('btn-', '');
        }
    });
});

const calculateButton = document.querySelector('#btn-calculate');
calculateButton.addEventListener('click', () => {
    if (firstOperand !== null && secondOperand !== null && currentOperation !== null) {
        const result = calculator.calculate(currentOperation, parseFloat(firstOperand), parseFloat(secondOperand));
        resultDisplay.textContent = result;
        firstOperand = result;
        secondOperand = null;
        currentOperation = null;
    }
});