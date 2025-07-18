// TeamA - Constantin Cristiana Georgiana - Badea Catalin Gabriel

// As folosi regiuni pentru structurarea codului, dar nu stiu daca o sa mearga bine cu checker-ul, ca am mai avut probleme :)
#include <iostream>
#include <stdlib.h>
#include <algorithm>
#include <vector>
#include <utility>
#include <queue>
#include <climits>
using namespace std;

// structuri
struct Tabla_struct {
    int N, M;
    int ** grid;
};
typedef Tabla_struct Tabla;

// nici eu nu stiu de ce le-am facut asa si nu cu vector<> de vector<>, dar nu vreau sa le mai schimb acum;
template<typename T>
T** alocTabla(int, int);
template<typename T>
void dealocaTabla(T**, int);

// operatii cu matrice
void readTabla(Tabla);
void initGrid(pair<int, int> **, int, int);
void initBoolGrid(bool **, int, int);
void afisTabla(Tabla);

// parte interesanta a codului ;D
vector<vector<pair<int, int>>> BFS_path(Tabla, pair<int,int>, pair<int,int>);   // foloseste DFS ca sa gasim toate drumurile de distanta minima de la S la T;
int BFS(Tabla, pair<int,int>, pair<int,int>, pair<int,int>);                    // BFS care ne da distanta minime sintre start si end. Il folosim ca sa il mutam pe E la urm pozitie din path;
void DFS(Tabla, pair<int, int>, pair<int, int>, bool**, vector<pair<int, int>>&, vector<vector<pair<int, int>>>&, const vector<pair<int, int>>&, int, int);

// functii utile
bool outOfBounds(pair<int,int>, Tabla);
pair<int, int> adunaPair(pair<int, int>, pair<int, int>);
void lowerPairBy1(pair<int, int> *_p); // pentru ca am indexat de la 0;

//------------------------------------------------------------------//

template<typename T>
T** alocTabla(int _N, int _M) {
    T** tabla = new T*[_N];
    for (int i = 0; i < _N; i++) {
        tabla[i] = new T[_M];
    }
    return tabla;
}

template<typename T>
void dealocaTabla(T** tabla, int N) {
    for (int i = 0; i < N; i++) {
        delete[] tabla[i];
    }
    delete[] tabla;
}



void readTabla(Tabla _t){
    for (int i = 0; i < _t.N; i++){
        for(int j = 0; j < _t.M; j++){
            cin >> _t.grid[i][j];
        }
    }
}

void initGrid(pair<int, int> ** _g, int _N, int _M) {
    for (int i = 0; i < _N; i++) {
        for (int j = 0; j < _M; j++) {
            _g[i][j] = {-1, -1}; 
        }
    }
}

void initBoolGrid(bool ** _g, int _N, int _M) {
    for (int i = 0; i < _N; i++) {
        for (int j = 0; j < _M; j++) {
            _g[i][j] = false; 
        }
    }
}

void afisTabla(Tabla _t){
    for (int i = 0; i < _t.N; i ++){
        for(int j = 0; j < _t.M; j++){
            cout << _t.grid[i][j] << " ";
        }
        cout << endl;
    }
}



vector<vector<pair<int, int>>> BFS_path(Tabla _t, pair<int, int> _start, pair<int, int> _end) {
    const vector<pair<int, int>> directii = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
    vector<vector<pair<int, int>>> allPaths;

    int distMin = BFS(_t, _start, _end, {-1, -1});  // aici e {-1,-1} pt ca folosim acelasi BFS, dar nu vrem sa tratam pozitia lui S ca un bloc, ca in cazul obisnuit, ci doar sa aflam distanta drumului minim;
    if (distMin == -1) { // daca nu exista drumuri;
        return allPaths;
    }

    bool **visited = alocTabla<bool>(_t.N, _t.M);
    initBoolGrid(visited, _t.N, _t.M);
    
    vector<pair<int, int>> currentPath;
    DFS(_t, _start, _end, visited, currentPath, allPaths, directii, distMin, 0);

    dealocaTabla(visited, _t.N);
    return allPaths;
}

int BFS(Tabla _t, pair<int, int> _start, pair<int, int> _end, pair<int, int> _S_currentPozition) {
    const vector<pair<int, int>> directii = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
    
    int moves = 0;
    bool finished = false;

    bool **grid_vizitat = alocTabla<bool>(_t.N, _t.M);
    initBoolGrid(grid_vizitat, _t.N, _t.M);
    
    queue<pair<int, int>> q;

    q.push(_start);
    grid_vizitat[_start.first][_start.second] = true;

    while (!q.empty()) {
        int noduri_in_pasul_urm = q.size();

        for (int i = 0; i < noduri_in_pasul_urm; i++) {
            pair<int, int> poz = q.front();
            q.pop();

            if (_end == poz) {
                finished = true;
                break;
            }

            for (int j = 0; j < 4; j++) {
                pair<int, int> nod_i = adunaPair(poz, directii[j]);

                if (outOfBounds(nod_i, _t)) continue;                   // daca pozitia e in afara e rau
                if (grid_vizitat[nod_i.first][nod_i.second]) continue;  // daca am vizitat deja pozitia e rau
                if (_t.grid[nod_i.first][nod_i.second] == 0) continue;  // daca pozitia e perete e rau
                if (nod_i == _S_currentPozition) continue;              // daca pozitia e S, nu are sens

                q.push(nod_i);
                grid_vizitat[nod_i.first][nod_i.second] = true;
            }
        }

        if (finished) {
            dealocaTabla(grid_vizitat, _t.N);
            return moves;
        }
        moves++;
    }

    dealocaTabla(grid_vizitat, _t.N);
    return -1;
}

void DFS(Tabla _t, pair<int, int> poz, pair<int, int> _end, bool** visited, vector<pair<int, int>>& currentPath, vector<vector<pair<int, int>>>& allPaths, const vector<pair<int, int>>& directii, int distMin, int distCurent) {
    if (poz == _end) {
        currentPath.push_back(_end);
        allPaths.push_back(currentPath);
        currentPath.pop_back();
        return;
    }

    if (distCurent > distMin) {
        return;
    }

    visited[poz.first][poz.second] = true;
    currentPath.push_back(poz);

    for (int i = 0; i < 4; i++) {
        pair<int, int> next = adunaPair(poz, directii[i]);

        if (outOfBounds(next, _t)) continue;
        if (visited[next.first][next.second]) continue;
        if (_t.grid[next.first][next.second] == 0) continue;

        DFS(_t, next, _end, visited, currentPath, allPaths, directii, distMin, distCurent + 1);
    }

    visited[poz.first][poz.second] = false;
    currentPath.pop_back();
}



// Ex: (2,3) linia 2, col 3;
bool outOfBounds(pair<int,int> _elem, Tabla _t){
    if(_elem.first < 0 || _elem.first >= _t.N || _elem.second < 0 || _elem.second >= _t.M){
        return true;
    }
    else return false;
}

pair<int, int> adunaPair(pair<int, int> p1, pair<int, int> p2) {
    return {p1.first + p2.first, p1.second + p2.second};
}

void lowerPairBy1(pair<int, int> *_p) {
    (*_p).first--;
    (*_p).second--;
}

//------------------------------------------------------------------//

int main(){
    vector<int> solutions;  // ca sa le afisam pe toate la final frumos;
    Tabla tabla;
    int K, Q;
    pair<int,int> E, S, T;

    cin >> tabla.N >> tabla.M >> K >> Q;
    tabla.grid = alocTabla<int>(tabla.N,tabla.M);
    readTabla(tabla);

    for(int q = 0; q < Q; q++){
        int solMin = INT_MAX;

        cin >> E.first >> E.second >> S.first >> S.second >> T.first >> T.second;
        lowerPairBy1(&E); // pentru ca in memorie sunt de la 0;
        lowerPairBy1(&S);
        lowerPairBy1(&T);

        // cautam toate drumurile de lungime minima posibile pentru a gasi cazul optim
        vector<vector<pair<int, int>>> drumuriST = BFS_path(tabla, S, T);
        if (drumuriST.size() == 0) {
            solutions.push_back(-1);
            continue;
        } else {
            for(unsigned int k = 0; k < drumuriST.size(); k++){
                pair<int,int> E_copy;                     // pentru fiecare drum avem nevoie de o copie a lui E
                int timpSolutie = 0;

                E_copy = E;
                for(unsigned int pas = 0; pas < drumuriST[k].size() - 1; pas++) {
                    int timpRotatie = BFS(tabla, E_copy, drumuriST[k][pas + 1], drumuriST[k][pas]);
                    
                    if (timpRotatie == -1 || timpRotatie >= K) {
                        timpSolutie += K;                 // trisam si mutam elem din drum in spatiul liber E;
                    } else {
                        timpSolutie += timpRotatie;       // ducem E la urmatoarea pozitie din drum;
                    }
                    E_copy = drumuriST[k][pas];           // mutam E in locul unde era S;
                    timpSolutie++;                        // mutam elem S mai departe in drum;
                }

                if(timpSolutie < solMin) {
                    solMin = timpSolutie;
                }
            }
        }
        solutions.push_back(solMin);
    }

    // afis final
    for (unsigned int i = 0; i < solutions.size(); i++) {
        cout << solutions[i] << "\n";
    }

    dealocaTabla(tabla.grid, tabla.N);
}

//------------------------------------------------------------------//
// Proble auxiliare folosite de mine :)
/*
4 6 10 1
1 0 1 1 1 1
1 0 1 1 1 0
1 1 0 1 1 1
0 1 1 1 1 1
4 6 2 3 3 1

4 6 10 1
1 0 1 1 1 1
1 1 1 0 1 0
1 1 0 0 1 1
0 1 1 1 1 1
4 6 2 3 3 1

3 3 10 1
1 1 1 
1 0 1 
1 1 1
1 1 1 3 3 1

3 3 10 1
1 1 1 
1 1 1 
1 1 1
1 1 1 3 3 1
*/