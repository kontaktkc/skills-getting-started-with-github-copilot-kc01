"""
Tests for prime number utilities
"""

import pytest
from src.prime_utils import is_prime, generate_first_n_primes, sum_of_first_n_primes


class TestIsPrime:
    """Tests for the is_prime function"""
    
    def test_is_prime_with_primes(self):
        """Test that known prime numbers return True"""
        assert is_prime(2) is True
        assert is_prime(3) is True
        assert is_prime(5) is True
        assert is_prime(7) is True
        assert is_prime(11) is True
        assert is_prime(13) is True
        assert is_prime(97) is True
    
    def test_is_prime_with_non_primes(self):
        """Test that known non-prime numbers return False"""
        assert is_prime(0) is False
        assert is_prime(1) is False
        assert is_prime(4) is False
        assert is_prime(6) is False
        assert is_prime(8) is False
        assert is_prime(9) is False
        assert is_prime(10) is False
        assert is_prime(100) is False
    
    def test_is_prime_with_negative(self):
        """Test that negative numbers return False"""
        assert is_prime(-1) is False
        assert is_prime(-5) is False


class TestGenerateFirstNPrimes:
    """Tests for the generate_first_n_primes function"""
    
    def test_first_5_primes(self):
        """Test generating first 5 prime numbers"""
        result = generate_first_n_primes(5)
        assert result == [2, 3, 5, 7, 11]
    
    def test_first_10_primes(self):
        """Test generating first 10 prime numbers"""
        result = generate_first_n_primes(10)
        assert result == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    def test_zero_primes(self):
        """Test generating zero primes"""
        result = generate_first_n_primes(0)
        assert result == []
    
    def test_negative_count(self):
        """Test generating negative count of primes"""
        result = generate_first_n_primes(-5)
        assert result == []
    
    def test_one_prime(self):
        """Test generating first prime number"""
        result = generate_first_n_primes(1)
        assert result == [2]


class TestSumOfFirstNPrimes:
    """Tests for the sum_of_first_n_primes function"""
    
    def test_sum_of_first_5_primes(self):
        """Test sum of first 5 primes: 2 + 3 + 5 + 7 + 11 = 28"""
        result = sum_of_first_n_primes(5)
        assert result == 28
    
    def test_sum_of_first_10_primes(self):
        """Test sum of first 10 primes: 2 + 3 + 5 + 7 + 11 + 13 + 17 + 19 + 23 + 29 = 129"""
        result = sum_of_first_n_primes(10)
        assert result == 129
    
    def test_sum_of_first_100_primes(self):
        """Test sum of first 100 primes"""
        result = sum_of_first_n_primes(100)
        # The 100th prime is 541, and the sum of first 100 primes is 24133
        assert result == 24133
    
    def test_sum_zero_primes(self):
        """Test sum of zero primes"""
        result = sum_of_first_n_primes(0)
        assert result == 0
    
    def test_sum_one_prime(self):
        """Test sum of first prime"""
        result = sum_of_first_n_primes(1)
        assert result == 2
