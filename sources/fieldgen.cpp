#include <iostream>
#include <vector>
#include <random>

double prob = 0.15;

std::pair<int, int> gencoords(std::mt19937& rnd, int l, int r) {
    int x = l + (rnd() % (r - l + 1));
    int y = l + (rnd() % (r - l + 1));
    return {x, y};
}

void print_help(const char *progname) {
    std::cerr << "Usage: " << progname << " t n p k [seed] [prob]\n t, n, p, k are values from the statement,\n seed is a seed value for random generator. If not provided, default value is used\n prob (in percents, in range [0; 50]) is a probability of generating wall in a cell\n  (i. e. approximately prob% of cells will be walls)\n If prob is not provided, it is set to 15\n";
}

int main(int argc, char *argv[]) {
    if (argc != 5 && argc != 6 && argc != 7) {
        print_help(argv[0]);
        return 1;
    }
    // std::mt19937 rnd;
    int t = atoi(argv[1]);
    int n = atoi(argv[2]);
    int p = atoi(argv[3]);
    int k = atoi(argv[4]);
    int seed = 0;
    if (argc >= 6) {
        seed = atoi(argv[5]);
    }
    std::mt19937 rnd(seed);
    if (argc == 7) {
        int prob_perc = atoi(argv[5]);
        if (prob_perc < 0 || prob_perc > 50) {
            std::cerr << "Invalid value of prob\n";
            print_help(argv[0]);
            return 1;
        } else {
            prob = prob_perc * 0.01;
        }
    }

    int a = 2 * (n + t / p) + 1;
    std::vector<std::vector<int>> vals(a, std::vector<int>(a));
    for (int i = 0; i < a; i++) {
        for (int j = 0; j < a; j++) {
            if (rnd() < prob * rnd.max()) {
                vals[i][j] = -1;
            }
        }
    }

    int l = a / 2 - n;
    int r = a / 2 + n;
    
    std::cout << t << ' ' << n << ' ' << p << ' ' << k << ' ' << a << '\n';
    for (int i = 0; i < a; i++) {
        for (int j = 0; j < a; j++) {
            std::cout << vals[i][j] << " \n"[j == a - 1];
        }
    }
    return 0;
}
