"""
Prime Number Utilities

This module provides functions for working with prime numbers,
including checking if a number is prime, generating prime numbers,
and calculating sums of prime numbers.
"""


def is_prime(n):
    """
    Check if a number is prime.
    
    Args:
        n (int): The number to check
        
    Returns:
        bool: True if n is prime, False otherwise
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    # Check for divisors up to sqrt(n)
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    
    return True


def generate_first_n_primes(n):
    """
    Generate the first n prime numbers.
    
    Args:
        n (int): The number of prime numbers to generate
        
    Returns:
        list: A list containing the first n prime numbers
    """
    if n <= 0:
        return []
    
    primes = []
    
    # Handle first prime (2) separately
    if n >= 1:
        primes.append(2)
    
    # Check odd numbers starting from 3
    candidate = 3
    while len(primes) < n:
        if is_prime(candidate):
            primes.append(candidate)
        candidate += 2  # Skip even numbers
    
    return primes


def sum_of_first_n_primes(n):
    """
    Calculate the sum of the first n prime numbers.
    
    Args:
        n (int): The number of prime numbers to sum
        
    Returns:
        int: The sum of the first n prime numbers
    """
    primes = generate_first_n_primes(n)
    return sum(primes)
