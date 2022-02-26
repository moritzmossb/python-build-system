#include "card.hpp"

Card::Card() {
    this -> name = "";
    this -> atk = 0;
    this -> def = 0;
    this -> life = 0;
    this -> alive = false;
}

Card::Card(std::string name, int atk, int def, int life) {
    this -> name = name;
    this -> atk = atk;
    this -> def = def;
    this -> life = life;
    this -> alive = true;
}

int Card::get_def() { return this -> def; }

void Card::life_delta (int delta) {
    int new_life = this -> life + delta;
    if ( new_life <= 0 ){
        this -> life = 0;
        this -> alive = false;
    }
    else this -> life = new_life;
}

void Card::attack(Card& target) {
    if ( this -> atk >= target.get_def() && target.alive ) {
        std::cout << this -> name << " attacks " << target.name << "\n";
        target.life_delta( this -> atk - target.get_def() );
        std::cout << target.name << " lost " << atk - target.get_def() << " hp\n";
    }
}