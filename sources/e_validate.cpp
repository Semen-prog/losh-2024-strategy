#include <format>
#include <fstream>
#include <iostream>
#include <string>
#include <utility>
#include <vector>

constexpr std::array<std::pair<int, int>, 4> construct_dirs() {
    std::array<std::pair<int, int>, 4> res;
    res[0] = {1, 0};
    res[1] = {-1, 0};
    res[2] = {0, 1};
    res[3] = {0, -1};
    return res;
}

constexpr std::array<std::pair<int, int>, 8> construct_all_dirs() {
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

namespace Validator {
    class Validator {
    private:
        enum statuses { OK = 0, PART = 1, FAIL = 2, LASTPART = 3, END = 4 };
        int t, n, p, k, a;
        std::vector<std::vector<int>> field;
        std::ofstream log_stream;
        int used_time = -1;
        std::vector<std::vector<int>> used;
        std::vector<std::pair<int, int>> dfs_used;

        constexpr static std::array<std::pair<int, int>, 4> dirs = construct_dirs();
        constexpr static std::array<std::pair<int, int>, 8> all_dirs = construct_all_dirs();

        inline std::pair<int, int> getij(int x, int y) {
            return std::make_pair(a / 2 - y, a / 2 + x);
        }

        inline std::pair<int, int> getcoords(int i, int j) {
            return std::make_pair(j - a / 2, a / 2 - i);
        }

        inline bool inside(int x, int y) {
            return (std::abs(x) <= n && std::abs(y) <= n);
        }

        inline std::pair<int, std::string> gen_status(statuses status, std::string&& message) {
            std::string res = "";
            if (status != OK && status != END) {
                res += message;
            }
            return std::make_pair(status, res);
        }

        void print_field() {
            log_stream << t << ' ' << n << ' ' << p << ' ' << k << ' ' << a << '\n';
            for (int i = 0; i < a; i++) {
                for (int j = 0; j < a; j++) {
                    log_stream << field[i][j] << " \n"[j == a - 1];
                }
            }
            log_stream << std::flush;
        }

        std::pair<int, std::string> validate_field() {
            int expansions = t / p;
            if (a != 2 * (n + expansions) + 1) {
                return gen_status(FAIL, "Incorrect A given\n");
            }

            std::vector<int> cnt_player_cells(k + 1);

            for (int i = 0; i < a; i++) {
                for (int j = 0; j < a; j++) {
                    auto [x, y] = getcoords(i, j);
                    if (field[i][j] > k) {
                        return gen_status(FAIL, std::format("Player number {} is bigger than k ({})\n", field[i][j], k));
                    }
                    if (!inside(x, y) && field[i][j] > 0) {
                        return gen_status(FAIL, std::format("Player {} has an initial position outside visible area\n", field[i][j]));
                    }
                    if (field[i][j] > 0) {
                        cnt_player_cells[field[i][j]]++;
                    }
                }
            }
            
            for (int i = 1; i <= k; i++) {
                if (cnt_player_cells[i] != 1) {
                    return gen_status(FAIL, std::format("Player {} has incorrect number of initial cells ({})\n", i, cnt_player_cells[i]));
                }
            }

            return gen_status(OK, "");
        }

        void expand_field() {
            n++;
            log_stream << "-1\n";
            for (int x = -n; x <= n; x++) {
                int y = n;
                auto [i, j] = getij(x, y);
                if (field[i][j] == -1) {
                    log_stream << 0 << ' ' << x << ' ' << y << '\n';
                }
                y = -n;
                std::pair<int, int> cres = getij(x, y);
                i = cres.first;
                j = cres.second;
                if (field[i][j] == -1) {
                    log_stream << 0 << ' ' << x << ' ' << y << '\n';
                }
            }
            for (int y = -n + 1; y < n; y++) {
                int x = -n;
                auto [i, j] = getij(x, y);
                if (field[i][j] == -1) {
                    log_stream << 0 << ' ' << x << ' ' << y << '\n';
                }
                x = n;
                std::pair<int, int> cres = getij(x, y);
                i = cres.first;
                j = cres.second;
                if (field[i][j] == -1) {
                    log_stream << 0 << ' ' << x << ' ' << y << '\n';
                }
            }
            log_stream << "-1\n";
            log_stream << std::flush;
        }

        bool dfs(int x, int y, int pl_num) {
            if (!inside(x, y)) {
                return true;
            }
            auto [i, j] = getij(x, y);
            if (used[i][j] == used_time || field[i][j] == pl_num) {
                return false;
            }
            used[i][j] = used_time;
            dfs_used.emplace_back(x, y);
            bool res = false;
            for (auto [dx, dy] : dirs) {
                res = res | dfs(x + dx, y + dy, pl_num);
            }
            return res;
        }

        std::pair<int, std::string> end_validation() {
            log_stream << -3 << std::endl;
            active = false;
            return gen_status(END, "");
        }

    public:
        bool active;

        Validator(const std::string& log_filename) : log_stream(log_filename) {
            active = true;
        }

        std::pair<int, std::string> init(int _t, int _n, int _p, int _k, int _a, const std::vector<std::vector<int>>& _field) {
            t = _t;
            n = _n;
            p = _p;
            k = _k;
            a = _a;
            field = _field;
            used.assign(a, std::vector<int>(a));
            dfs_used.reserve(a * a);
            print_field();

            return validate_field();
        }

        std::pair<int, std::string> validate_input(int pl_num, int x, int y) {
            if (pl_num == -1) {
                expand_field();
                return gen_status(OK, "");
            }
            if (pl_num == -3) {
                return end_validation();
            }
            if (!inside(x, y)) {
                return gen_status(PART, std::format("Player {} has made incorrect move: cell is outside visible area\n", pl_num));
            }
            auto [i, j] = getij(x, y);
            if (field[i][j] != 0) {
                return gen_status(PART, std::format("Player {} has made incorrect move: cell is not empty\n", pl_num));
            }
            int cnt_near = 0;
            for (auto [dx, dy] : all_dirs) {
                if (inside(x + dx, y + dy)) {
                    auto [ni, nj] = getij(x + dx, y + dy);
                    if (field[ni][nj] == pl_num) {
                        cnt_near++;
                    }
                }
            }
            if (cnt_near <= 1) {
                field[i][j] = pl_num;
                log_stream << pl_num << ' ' << x << ' ' << y << std::endl;
                return gen_status(OK, "");
            } else {
                field[i][j] = pl_num;
                used_time++;
                log_stream << pl_num << ' ' << x << ' ' << y << "\n";
                log_stream << "-2\n";
                for (auto [dx, dy] : all_dirs) {
                    if (!dfs(x + dx, y + dy, pl_num)) {
                        for (const auto& curel : dfs_used) {
                            auto [ci, cj] = getij(curel.first, curel.second);
                            if (field[ci][cj] != -1) {
                                field[ci][cj] = pl_num;
                                auto [x, y] = getcoords(ci, cj);
                                log_stream << pl_num << ' ' << x << ' ' << y << std::endl;
                            }
                        }
                        dfs_used.resize(0);
                    } else {
                        dfs_used.resize(0);
                    }
                }
                log_stream << "-2\n";
                return gen_status(OK, "");
            }
        }

        inline std::vector<int> get_player_scores() {
            std::vector<int> res(k + 1);
            for (int i = 0; i < a; i++) {
                for (int j = 0; j < a; j++) {
                    if (field[i][j] > 0) {
                        res[field[i][j]]++;
                    }
                }
            }
            return res;
        }
    };
} // namespace Validator

int main(int argc, char *argv[]) {
    if (argc < 2) {
        std::cerr << "Not enough parameters\n";
        return 0;
    }
    std::string log_filename(argv[1]);
    Validator::Validator validator(log_filename);

    int t, n, p, k, a;
    std::cin >> t >> n >> p >> k >> a;
    std::vector<std::vector<int>> field(a, std::vector<int>(a));
    for (int i = 0; i < a; i++) {
        for (int j = 0; j < a; j++) {
            std::cin >> field[i][j];
        }
    }

    auto [field_status, field_comment] = validator.init(t, n, p, k, a, field);
    std::cout << field_status << '\n' << field_comment << std::flush;
    
    while (validator.active) {
        int pl, x, y;
        std::cin >> pl >> x >> y;
        const auto& [status, comment] = validator.validate_input(pl, x, y);
        std::cout << status << '\n' << comment << std::flush;
    }

    std::vector<int> scores = validator.get_player_scores();

    for (int i = 1; i <= k; i++) {
        std::cout << scores[i] << " \n"[i == k];
    }

    return 0;
}
