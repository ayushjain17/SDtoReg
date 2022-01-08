def power(x, y, p):
    res = 1;  # Initialize result
    x = x % p;  # Update x if it is more
    # than or equal to p
    while (y > 0):

        # If y is odd, multiply
        # x with result
        if (y & 1):
            res = (res * x) % p;

        # y must be even now
        y = y >> 1;  # y = y/2
        x = (x * x) % p;

    return res


# Function to find modular inverse
# of a under modulo p using Fermat's
# method. Assumption: p is prime
def modInverse(a, p):
    return power(a, p - 2, p)


fact = {0: 1}
m = 0

# Returns n! % p using
# Wilson's Theorem
def modFact(n, p):
    # n! % p is 0 if n >= p
    global fact, m
    if p <= n:
        return 0
    if n < m:
        return fact[n]
    for i in range(m+1, n+1):
        fact[i] = (fact[i-1] * i) % p
    m = n
    return fact[n]

def func(x)


if __name__ == '__main__':
    T = int(input())
    while T > 0:
        N = int(input())
        print(modFact(int(N/2), 1000000007), modFact(int((N+1)/2), 1000000007))