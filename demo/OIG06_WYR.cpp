#include <bits/stdc++.h>

int main()
{
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);

    std::string s; std::cin>>s;
    char prev_letter = s[1];
    std::cout<<prev_letter;
    for (auto c: s)
    {
        if(c == prev_letter) continue;
        
        std::cout<<c;
        prev_letter = c;
    }
}
