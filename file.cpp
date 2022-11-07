#include <bits/stdc++.h>
using namespace std;

int binSearchLowerBound(int *tab, int n, int number)
{
    int l = 0;
    int r = n - 1;
    int mid = 0;
    while (l < r)
    {
        mid = (l + r) / 2;
        if (tab[mid] >= number)
            r = mid;
        else
            l = mid + 1;
    }
    return l;
}

int binSearchUpperBound(int *tab, int n, int number)
{
    int l = 0;
    int r = n - 1;
    int mid = 0;
    while (l < r)
    {
        mid = (l + r + 1) / 2;
        if (tab[mid] <= number)
            l = mid;
        else
            r = mid - 1;
    }
    return l;
}

int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int t;
    cin >> t;
    while (t--)
    {
        int n;
        cin >> n;
        int tab[n];
        for (int i = 0; i < n; i++)
            cin >> tab[i];
        int q;
        cin >> q;
        sort(tab, tab + n);
        while (q--)
        {
            int a, b;
            cin >> a >> b;
            int lowerBound = binSearchLowerBound(tab, n, a);
            int upperBound = binSearchUpperBound(tab, n, b);
            if (tab[upperBound] > b)
                cout << "0\n";
            else if (tab[lowerBound] < a)
                cout << "0\n";
            else
                cout << upperBound - lowerBound + 1 << "\n";
        }
    }
}