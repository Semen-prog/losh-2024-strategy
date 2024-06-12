#include <bits/stdc++.h>
#define cerr if(false)cerr 

using namespace std;

// const vector<pair<int, int>> only_paths = {
//     {0, 1}, {0, -1},
//     {1, 0}, {-1, 0}  
// };

// const vector<pair<int, int>> paths = {
//     {0, 1}, {0, -1},
//     {1, 0}, {-1, 0},
//     {-1, -1}, {-1, 1},
//     {1, -1}, {1, 1}
// };

constexpr std::array<std::pair<int, int>, 4> construct_only_paths() {
    std::array<std::pair<int, int>, 4> res;
    res[0] = {1, 0};
    res[1] = {-1, 0};
    res[2] = {0, 1};
    res[3] = {0, -1};
    return res;
}

constexpr std::array<std::pair<int, int>, 8> construct_paths() {
    std::array<std::pair<int, int>, 8> res;
    res[0] = {1, 0};
    res[1] = {-1, 0};
    res[2] = {1, 1};
    res[3] = {-1, 1};
    res[4] = {1, -1};
    res[5] = {-1, -1};
    res[6] = {0, 1};
    res[7] = {0, -1};
    return res;
}

constexpr std::array<std::pair<int, int>, 4> only_paths = construct_only_paths();
constexpr std::array<std::pair<int, int>, 8> paths = construct_paths();

ofstream out;

int t, n, p, k, a;
vector<vector<int>> tab, used;
vector<bool> alive;
int num_players, num_days, tmp_player, tmp_size, used_time;
bool extended;

int flag = 0;
string comment;

pair<int, int> get_cell(int x, int y) {
    return { -y + a, x + a };
}

bool correct(int x, int y) {
    return abs(x) <= tmp_size && abs(y) <= tmp_size;
}

void check_error() {
    cerr << "stepped into check_error()" << endl;
    if (flag == 0) {
        cerr << "Writing 0" << endl;
        cout << 0 << endl;
    } else if (flag == 4) {
        cerr << "Writing 4" << endl;
        cout << 4 << endl;
        vector<int> scores(k, 0);
        for (int x = -tmp_size; x <= tmp_size; ++x) {
            for (int y = -tmp_size; y <= tmp_size; ++y) {
                auto [i, j] = get_cell(x, y);
                if (tab[i][j] > 0) scores[tab[i][j] - 1]++;
            }
        }
        for (int i = 0; i < k; ++i) cout << scores[i] << ' ';
        cout << endl;
        out << -3 << endl;
        out.close();
        exit(0);
    } else {
        cerr << "Writing " << flag << endl;
        cout << flag << '\n' << comment << endl;
        if (flag == 2) {
            out << "Error: " << comment << endl;
            out.close();
            exit(0);
        }
    }
    flag = 0;
    comment = "";
}

void next_alive(int next) {
    for (tmp_player = (tmp_player + 1) % k; tmp_player != next - 1; tmp_player = (tmp_player + 1) % k) {
        if (tmp_player == 0) {
            num_days++;
            cerr << "New day!\n";
            if (num_days % p == 0 && !extended) {
                flag = 2;
                comment = "Field was not extended";
                check_error();
            }
        }
        alive[tmp_player] = false;
    }
    if (tmp_player == 0) {
        num_days++;
        cerr << "New day!\n";
        if (num_days % p == 0 && !extended) {
            flag = 2;
            comment = "Field was not extended";
            check_error();
        }
    }
}

void kill(int num, string comm) {
    alive[num - 1] = false;
    if (--num_players == 0) {
        flag = 3;
    } else {
        flag = 1;
    }
    comment = comm;
}

bool find(int x, int y, int num) {
    if (!correct(x, y)) return true;
    auto [i, j] = get_cell(x, y);
    if (used[i][j] >= used_time || tab[i][j] == num) return false;
    used[i][j] = used_time;
    bool res = false;
    for (auto [dx, dy]: only_paths) {
        if (find(x + dx, y + dy, num)) res = true;
    }
    return res;
}

void paint(int x, int y, int num) {
    if (!correct(x, y)) return;
    auto [i, j] = get_cell(x, y);
    if (used[i][j] == used_time + 1 || tab[i][j] == num) return;
    used[i][j] = used_time + 1; 
    if (tab[i][j] != -1 && tab[i][j] != num) {
        tab[i][j] = num;
        out << num << " " << x << " " << y << endl;
    }
    for (auto [dx, dy]: only_paths) {
        paint(x + dx, y + dy, num);
    }
}

void check_turn(int num, int x, int y) {
    cerr << "Turn checking..." << endl;
    if (num == 0) {
        flag = 2;
        comment = "'0 x y' is forbidden here";
        return;
    }
    cerr << "num != 0" << endl;
    if (num < 0 || num > k) {
        flag = 2;
        comment = "Incorrect value";
        return;
    }
    cerr << "num >= && num <= k" << endl;
    if (!alive[num - 1]) {
        flag = 2;
        comment = "Walking Dead! SOS!";
        return;
    }
    cerr << "alive[num - 1]" << endl;
    next_alive(num);
    cerr << "finished next alive" << endl;
    if (!correct(x, y)) {
        cerr << "incorrect, killing" << endl;
        kill(num, "Attempt to use invisible cell");
        return;
    }
    cerr << "correct" << endl;
    auto [i, j] = get_cell(x, y);
    if (tab[i][j] != 0) {
        cerr << "tab[i][j] != 0" << endl;
        kill(num, "Attempt to use non-empty cell");
        return;
    }
    cerr << "tab[i][j] == 0" << endl;
    cerr << "writing " << num << ' ' << x << ' ' << y << endl;
    out << num << " " << x << " " << y << endl;
    tab[i][j] = num;
    out << -2 << endl;
    int cnt = 0;
    for (auto [dx, dy]: paths) {
        auto [ii, jj] = get_cell(x + dx, y + dy);
        if (tab[ii][jj] == num) cnt++;
    }
    if (cnt >= 2) {
        used_time++;
        for (auto [dx, dy]: paths) {
            auto [ii, jj] = get_cell(x + dx, y + dy);
            if (tab[ii][jj] != num && used[ii][jj] < used_time) {
                if (!find(x + dx, y + dy, num)) paint(x + dx, y + dy, num);
            }
        }
        used_time++;
    }
    out << -2 << endl;
    cerr << "exiting from check_turn()" << endl;
}

void init() {
    cin >> t >> n >> p >> k >> a; a /= 2;
    tmp_size = n;
    pair<int, int> infp(INT32_MAX, INT32_MAX);
    vector<pair<int, int>> start(k, infp);
    tab.assign(2 * a + 1, vector<int>(2 * a + 1, 0));
    out << t << " " << n << " " << p << " " << k << " " << a << endl;
    for (int y = a; y >= -a; --y) {
        for (int x = -a; x <= a; ++x) {
            int val; cin >> val;
            if (val < -1 || val > k) {
                flag = 2;
                comment = "Incorrect cell value";
            }
            auto [i, j] = get_cell(x, y);
            tab[i][j] = val;
            out << val << ' ';
            if (correct(x, y) && val > 0) {
                if (start[val - 1] != infp) {
                    flag = 2;
                    comment = "There are two or more start points for player " + to_string(val);
                }
                start[val - 1] = { x, y };
            } else if (val > 0) {
                flag = 2;
                comment = "Start point for player " + to_string(val) + " is not in visible part";
            }
        }
        out << endl;
    }
    for (int i = 0; i < k; ++i) {
        if (start[i] == infp) {
            flag = 2;
            comment = "There is no start point for player " + to_string(i + 1);
        }
    }
    if (a < n + t / p) {
        flag = 2;
        comment = "Field must be bigger";
    }
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        cerr << "Validator: Incorrect usage!" << endl;
        return 0;
    }
    freopen("logs/validate.log", "w", stderr);
    out.open(argv[1]);
    init(); check_error();
    used.assign(2 * a + 1, vector<int>(2 * a + 1, 0));
    num_players = k, num_days = 0, tmp_player = -1, tmp_size = n;
    alive.assign(k, true);
    while (true) {
        int num, x, y;
        cin >> num >> x >> y;
        cerr << "Validator info " << num << ' ' << x << ' ' << y << endl;
        if (num == -3 && x == -3 && y == -3) {
            flag = 4;
        } else if (num_days > t) {
            cerr << "num_days > t" << endl;
            flag = 2;
            comment = "Unable to continue the game";
        } else if (num == -1 && x == -1 && y == -1) {
            if ((num_days + 1) % p != 0) {
                flag = 2;
                comment = "Field extension is forbidden here";
            } else {
                out << -1 << endl;
                tmp_size++;
                extended = true;
                for (int _x = -tmp_size; _x < tmp_size; ++_x) {
                    auto [i, j] = get_cell(_x, -tmp_size);
                    if (tab[i][j] == -1) out << "0 " << _x << ' ' << -tmp_size << endl;
                }
                for (int _y = -tmp_size; _y < tmp_size; ++_y) {
                    auto [i, j] = get_cell(tmp_size, _y);
                    if (tab[i][j] == -1) out << "0 " << tmp_size << ' ' << _y << endl;
                }
                for (int _x = tmp_size; _x > -tmp_size; --_x) {
                    auto [i, j] = get_cell(_x, tmp_size);
                    if (tab[i][j] == -1) out << "0 " << _x << ' ' << tmp_size << endl;
                }
                for (int _y = tmp_size; _y > -tmp_size; --_y) {
                    auto [i, j] = get_cell(-tmp_size, _y);
                    if (tab[i][j] == -1) out << "0 " << -tmp_size << ' ' << _y << endl;
                }
                for (int i = tmp_player + 1; i < k; ++i) {
                    alive[i] = false;
                    if (alive[i]) --num_players;
                }
                out << -1 << endl;
                if (num_players == 0) {
                    flag = 3;
                    comment = "New day and no players";
                }
            }
        } else {
            check_turn(num, x, y);
            extended = false;
        }
        check_error();
    }
}
