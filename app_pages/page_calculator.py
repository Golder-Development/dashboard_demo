import streamlit as st

def calculator_body():
    st.write("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        num1 = st.number_input(label="Enter the first number", step=1)
    with col2:
        num2 = st.number_input(label="Enter the second number", step=1)
    with col3:
        operation = st.selectbox(label="Select an operation", 
                                 options=["Addition", "Subtraction", "Multiplication", "Division"])
        
    if st.button("Click here for the maths"):
        if num2 == 0 and operation == "Division":
            st.error("Cannot divide by zero. Try again.")
        else:
            calculator_function(num1, num2, operation)


def calculator_function(num1, num2, operation):
    """
    Perform a mathematical operation on two numbers.

    Parameters:
    - num1 (float): The first number.
    - num2 (float): The second number.
    - operation (str): The operation to perform. Valid options are "Addition", "Subtraction", "Multiplication", and "Division".

    Returns:
    - None

    Raises:
    - None
    """
    if operation == "Addition":
        result = num1 + num2
        st.success(f"The sum of {num1} and {num2} is **{result}**")
    elif operation == "Subtraction":
        result = num1 - num2
        st.success(f"The difference between {num1} and {num2} is **{result}**")
    elif operation == "Multiplication":
        result = num1 * num2
        st.success(f"The product of {num1} and {num2} is **{result}**")
    elif operation == "Division":
        result = num1 / num2
        st.success(f"The quotient of {num1} and {num2} is **{result}**")
    else:
        st.error("Invalid operation. Please try again.")
    
