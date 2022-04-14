#ifndef CARD_HPP
#define CARD_HPP

#include <string>
#include <iostream>

class Card {
    private:
        int atk;
        int def;
        int life;
    public:
        std::string name;
        bool alive;
        Card();
        Card(std::string name, int atk, int def, int life);
        void attack(Card& target);

        int get_def();
        void life_delta(int delta);
};

#endif