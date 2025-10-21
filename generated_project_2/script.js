// Function to perform addition
function add(num1, num2) {
    return num1 + num2;
}

// Function to perform subtraction
function subtract(num1, num2) {
    return num1 - num2;
}

// Function to perform multiplication
function multiply(num1, num2) {
    return num1 * num2;
}

// Function to perform division
function divide(num1, num2) {
    if (num2 === 0) {
        alert("Cannot divide by zero");
        return null;
    }
    return num1 / num2;
}

// Function to update the display
function updateDisplay(result) {
    const display = document.getElementById('result-display');
    display.value = result;
}

// Function to handle button click
function handleOperation(operation) {
    const num1 = parseFloat(document.getElementById('number1').value);
    const num2 = parseFloat(document.getElementById('number2').value);
    let result;

    switch (operation) {
        case 'add':
            result = add(num1, num2);
            break;
        case 'subtract':
            result = subtract(num1, num2);
            break;
        case 'multiply':
            result = multiply(num1, num2);
            break;
        case 'divide':
            result = divide(num1, num2);
            break;
        default:
            result = null;
    }
    
    updateDisplay(result);
}

// Adding event listeners to buttons
document.getElementById('add').addEventListener('click', () => handleOperation('add'));
document.getElementById('subtract').addEventListener('click', () => handleOperation('subtract'));
document.getElementById('multiply').addEventListener('click', () => handleOperation('multiply'));
document.getElementById('divide').addEventListener('click', () => handleOperation('divide'));
