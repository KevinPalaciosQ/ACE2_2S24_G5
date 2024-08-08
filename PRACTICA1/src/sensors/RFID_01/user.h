#ifndef USER_H
#define USER_H

#include <Arduino.h> // Asegúrate de incluir esta línea para que String y bool funcionen

class User {
  private:
    String pin;
    bool state;
  public:
    User(String pin);
    bool getState();
    void setState(bool state);
    String getPin();
};

#endif
