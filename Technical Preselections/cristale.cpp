// TeamA - Constantin Cristiana Georgiana - Badea Catalin Gabriel
#include <iostream>
#include <vector>

using namespace std;

bool solveGame (int); // returns true daca castiga Arin

//------------------------------------------------------------------//

bool solveGame (int _T){
    vector<int> mutari {2,5,7};
    vector<bool> pozitii(_T + 1, false);
    pozitii[0] = pozitii[1] = false; // adica lose pentru cine e in pozitia asta;
    for(int pas = 1; pas<= _T; pas++){
        for(int m : mutari){
            if(pas - m >= 0){
                if(pozitii[pas-m] == false) 
                {
                    pozitii[pas] = true;
                    break;
                }
            }
        }
    }
    return pozitii[_T];
}

//------------------------------------------------------------------//

int main(){
    int n;
    cin >> n;
    for(int i = 0; i<n; i++){
        int T;
        cin >> T;
        if(solveGame(T)) cout << "Arin\n";     // Arin e primul;
        else cout << "Bion\n";                 // Bion e al doilea;
    }
    return 0;
}