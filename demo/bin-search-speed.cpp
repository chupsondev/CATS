#include <bits/stdc++.h>

constexpr long long MAX_SEARCHED = 1e12 + 10;

long long find_linear(long long n) {
    long long i = 1;
    for(i; i <= n; i++) {
        int a = 1;
        int b = 3;
        int c = a + b;
    }
    return i - 1;
}

long long bin_search(long long n, bool verbose = false) {
    long long l = 1;
    long long r = MAX_SEARCHED;

    int i = 0;

    while(r - l > 1) {
        i++;
        long long mid = (r + l) / 2;
        if(verbose) std::cout << "Zakres: " << l << "-" << r << " | Środek: " << mid << '\n'; 
        if(n > mid) l = mid;
        else r = mid;
    }
    std::cout << "Znaleziona liczba " << r << '\n';
    return i;
}

int main(int argc, char *argv[]) {
    if(argc <= 1) {
        std::cout << "You must provide a number to be guessed" << '\n';
        return 1;
    } 

    long long n = std::atoll(argv[1]);
    bool verbose = false;
    if(argc >= 2) {
        std::string arg = argv[2];
        if (arg == "-v") {
            std::cout << "Verbose mode." << '\n';
            verbose = true;
        }
    }

    std::cout << "Wyszukiwanie wolną metodą: " << '\n';
    long long operations_linear = find_linear(n);
    std::cout << "Skończono wyszukiwać. Zajęło to w przybliżeniu " << operations_linear << " operacji" << '\n';
    std::cout << "Kliknij enter aby zacząć bin search" << '\n';
    std::cin.get();
    std::cout << "Wyszukiwanie metodą bin search: " << '\n';
    long long operations_bs = bin_search(n, verbose);
    std::cout << "Skończono wyszukiwać. Zajęło to w przybliżeniu " << operations_bs << " operacji" << '\n';
}