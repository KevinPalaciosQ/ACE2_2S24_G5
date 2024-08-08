#include "User.h"

User::User(String pin) {
  this->pin = pin;
  this->state = false;
}

bool User::getState() {
  return this->state;
}

void User::setState(bool state) {
  this->state = state;
}

String User::getPin() {
  return this->pin;
}
