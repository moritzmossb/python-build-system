#include <iostream>

#include "card/card.hpp"


int main(void) {
    Card wolf("Wolf", 5, 2, 10);
    Card bear("Bear", 4, 3, 15);

    Card& attacker = wolf;
    Card& target = bear;
    Card& tmp = wolf;

    while (wolf.alive or bear.alive) {
        attacker.attack(target);
        tmp = attacker;
        attacker = target;
        target = tmp;
    }
}