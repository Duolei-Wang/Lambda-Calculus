#include "STLC.h"


int main() {
    auto zero = Zero();
    auto one = Succ{zero};
    cout << one.toString();
    return 0;
}
