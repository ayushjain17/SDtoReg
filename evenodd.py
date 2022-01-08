fact = {0: 1}
m = 0


def modFact(n):
    global fact, m
    if 1000000007 <= n:
        return 0
    if n < m:
        return fact[n]
    for i in range(m + 1, n + 1):
        fact[i] = (fact[i - 1] * i) % 1000000007
    m = n
    return fact[n]


def ncr(n, r):
    return int(modFact(n)/(modFact(n - r)*modFact(r)))


if __name__ == '__main__':
    T = int(input())
    while T > 0:
        N = int(input())
        even = 0
        odd = 0
        for i in range(1, N+1):
            if i % 2 == 1:
                odd += ncr(N, i) % 1000000007
            else:
                even += ncr(N, i) % 1000000007
        print(even, odd)
        print((2**(N-1)-1) % 1000000007, (2**(N-1)) % 1000000007)
phsts escdcluosh oetc iytecka re
