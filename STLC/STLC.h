//
// Created by Lin Mulikas on 2024/1/22.
//
#ifndef STLC_STLC_H
#define STLC_STLC_H

#include <string>
#include <iostream>

using std::string;
using std::cout, std::endl;

enum class patternTerm {
    Quote, Zero, Succ, Abstraction, Application, Mu
};

class Term {
private:
    patternTerm t;
    string name;
public:
    Term() {}

    Term(patternTerm x) : t(x) {}

    Term(string x) : t(patternTerm::Quote), name(x) {}

    Term(patternTerm pt, string x) : t(pt), name(x) {}

    virtual string toString() {
        return "No implement";
    }
};

class Zero : public Term {
public:
    Zero() : Term(patternTerm::Zero) {}

    string toString() override {
        return string{"zero"};
    }

    friend std::ostream &operator<<(std::ostream &os, Zero &term) {
        cout << "zero" << endl;
        return os;
    }
};

class Succ : public Term {
private:
    Term &M;
public:
    explicit Succ(Term &t) : Term(patternTerm::Succ), M(t) {}

    string toString() override {
        return string{"succ "} + M.toString();
    }

    friend std::ostream &operator<<(std::ostream &os, Succ &term) {
        cout << "succ ";
        cout << term.M.toString();
        return os;
    }
};

#endif //STLC_STLC_H
