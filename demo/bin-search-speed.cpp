#include <bits/stdc++.h>
#include <Windows.h>
#include <cstdio>


long long find_linear(long long n) {
    long long i = 1;
    for (i; i <= n; i++) {
        int a = 1;
        int b = 3;
        int c = a + b;
    }
    return i - 1;
}

long long bin_search(long long n, bool verbose = false) {
    long long l = 1;
    long long r = n;

    long long i = 0;

    while (r - l > 1) {
        i++;
        long long mid = (r + l) / 2;
        if (verbose)
            std::cout << "Zakres: " << l << "-" << r << " | Środek: " << mid
                      << '\n';
        if (n > mid)
            l = mid;
        else
            r = mid;
    }
    long long res = l == n ? l : r;
    std::cout << "Znaleziona liczba " << res << '\n';
    return i;
}

int main(int argc, char *argv[]) {
        // Set console code page to UTF-8 so console known how to interpret string data
    SetConsoleOutputCP(CP_UTF8);



    long long n;
    bool verbose;
     if (argc <= 1) {
        std::cout << "Podaj liczbę do zgadnięcia" << '\n';
        std::cin >> n;
        std::cout << "Czy pokazać proces bin search? (y/n)" << '\n';
        char c;
        std::cin >> c;
        verbose = c == 'y';
    }
    else {
        n = std::atoll(argv[1]);
        verbose = false;
        if (argc > 2) {
            std::string arg = argv[2];
            if (arg == "-v") {
                std::cout << "Verbose mode." << '\n';
                verbose = true;
            }
        }
    }

    if(n > 1e9) {
        std::cout << "Wyszukiwanie tej liczby wolną metodą zajęło by zbyt dużo czasu. Pokażemy, że bin search i tak wyszuka ją szybko." << '\n';
        int ops = bin_search(n, verbose);
        std::cout << "Wykonano " << ops << " operacji." << '\n';
        return 0;
    }

    std::cout << "Wyszukiwanie wolną metodą: " << '\n';
    long long operations_linear = find_linear(n);
    std::cout << "Skończono wyszukiwać. Zajęło to w przybliżeniu "
              << operations_linear << " operacji" << '\n';
    std::cout << "Kliknij enter aby zacząć bin search" << '\n';
    std::cin.clear();
    std::cin.ignore(1);
    std::cin.get();
    std::cout << "Wyszukiwanie metodą bin search: " << '\n';
    long long operations_bs = bin_search(n, verbose);
    std::cout << "Skończono wyszukiwać. Zajęło to w przybliżeniu "
              << operations_bs << " operacji" << '\n';
}
