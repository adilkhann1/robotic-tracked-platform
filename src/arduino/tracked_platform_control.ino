#include <IBusBM.h>

IBusBM ibus;

// =====================================
// ПИНЫ
// =====================================
const int LEFT_LPWM  = 3;
const int LEFT_RPWM  = 2;

const int RIGHT_LPWM = 4;
const int RIGHT_RPWM = 5;

const int LEFT_EN1   = 22;
const int LEFT_EN2   = 23;
const int RIGHT_EN1  = 24;
const int RIGHT_EN2  = 25;

// =====================================
// КАНАЛЫ ПУЛЬТА
// =====================================
const int CH_THR   = 3;   // CH3 - газ
const int CH_STEER = 2;   // CH4 - поворот
const int CH_ARM   = 5;   // CH6 / SwC

// =====================================
// ЦЕНТРЫ
// Сначала ставим стандартные, потом поправим по Serial
// =====================================
const int CENTER_THR   = 1500;
const int CENTER_STEER = 1500;

// =====================================
// НАСТРОЙКИ
// =====================================
const int DEADZONE_THR   = 140;
const int DEADZONE_STEER = 120;

const int MAX_PWM_LIMIT = 110;
const int MIN_PWM_START = 65;
const int SLEW_STEP     = 6;

const int ARM_THRESHOLD = 1700;
const int CH_MIN_VALID  = 850;
const int CH_MAX_VALID  = 2150;

// =====================================
int currentLeftPWM  = 0;
int currentRightPWM = 0;

// =====================================
bool channelsAreValid(int a, int b, int d) {
  return (a >= CH_MIN_VALID && a <= CH_MAX_VALID &&
          b >= CH_MIN_VALID && b <= CH_MAX_VALID &&
          d >= CH_MIN_VALID && d <= CH_MAX_VALID);
}

bool isArmed(int chArm) {
  return chArm > ARM_THRESHOLD;
}

int applyDeadzone(int value, int center, int deadzone) {
  int delta = value - center;
  if (abs(delta) < deadzone) return 0;
  return delta;
}

int mapDeltaToPWM(int delta, int inRange, int outMax) {
  delta = constrain(delta, -inRange, inRange);
  int pwm = map(delta, -inRange, inRange, -outMax, outMax);

  if (pwm > 0) {
    pwm = map(pwm, 1, outMax, MIN_PWM_START, outMax);
  } else if (pwm < 0) {
    pwm = map(pwm, -outMax, -1, -outMax, -MIN_PWM_START);
  }

  return pwm;
}

int slewToTarget(int currentValue, int targetValue, int stepSize) {
  if (currentValue < targetValue) {
    currentValue += stepSize;
    if (currentValue > targetValue) currentValue = targetValue;
  } else if (currentValue > targetValue) {
    currentValue -= stepSize;
    if (currentValue < targetValue) currentValue = targetValue;
  }
  return currentValue;
}

void stopMotors() {
  currentLeftPWM = 0;
  currentRightPWM = 0;

  analogWrite(LEFT_LPWM, 0);
  analogWrite(LEFT_RPWM, 0);
  analogWrite(RIGHT_LPWM, 0);
  analogWrite(RIGHT_RPWM, 0);
}

void driveOneMotor(int lpwmPin, int rpwmPin, int pwmValue) {
  pwmValue = constrain(pwmValue, -255, 255);

  if (pwmValue > 0) {
    analogWrite(lpwmPin, pwmValue);
    analogWrite(rpwmPin, 0);
  } else if (pwmValue < 0) {
    analogWrite(lpwmPin, 0);
    analogWrite(rpwmPin, -pwmValue);
  } else {
    analogWrite(lpwmPin, 0);
    analogWrite(rpwmPin, 0);
  }
}

void setup() {
  Serial.begin(115200);
  Serial1.begin(115200);
  ibus.begin(Serial1);

  pinMode(LEFT_LPWM, OUTPUT);
  pinMode(LEFT_RPWM, OUTPUT);
  pinMode(RIGHT_LPWM, OUTPUT);
  pinMode(RIGHT_RPWM, OUTPUT);

  pinMode(LEFT_EN1, OUTPUT);
  pinMode(LEFT_EN2, OUTPUT);
  pinMode(RIGHT_EN1, OUTPUT);
  pinMode(RIGHT_EN2, OUTPUT);

  digitalWrite(LEFT_EN1, HIGH);
  digitalWrite(LEFT_EN2, HIGH);
  digitalWrite(RIGHT_EN1, HIGH);
  digitalWrite(RIGHT_EN2, HIGH);

  stopMotors();

  Serial.println("FLYSKY TANK TEST");
  Serial.println("CH3=THROTTLE, CH4=STEER, CH6=ARM/SAFE");
}

void loop() {
  ibus.loop();

  int chThr   = ibus.readChannel(CH_THR);   // CH3
  int chSteer = ibus.readChannel(CH_STEER); // CH4
  int chArm   = ibus.readChannel(CH_ARM);   // CH6

  if (!channelsAreValid(chThr, chSteer, chArm) || !isArmed(chArm)) {
    stopMotors();
    delay(20);
    return;
  }

  int thrDelta   = applyDeadzone(chThr, CENTER_THR, DEADZONE_THR);
  int steerDelta = applyDeadzone(chSteer, CENTER_STEER, DEADZONE_STEER);

  int thrPWM = 0;
  int steerPWM = 0;

  if (thrDelta != 0) {
    thrPWM = mapDeltaToPWM(thrDelta, 600, MAX_PWM_LIMIT);
  }

  if (steerDelta != 0) {
    steerPWM = mapDeltaToPWM(steerDelta, 600, MAX_PWM_LIMIT);
  }

  int targetLeftPWM  = thrPWM + steerPWM;
  int targetRightPWM = thrPWM - steerPWM;

  targetLeftPWM  = constrain(targetLeftPWM,  -MAX_PWM_LIMIT, MAX_PWM_LIMIT);
  targetRightPWM = constrain(targetRightPWM, -MAX_PWM_LIMIT, MAX_PWM_LIMIT);

  currentLeftPWM  = slewToTarget(currentLeftPWM,  targetLeftPWM,  SLEW_STEP);
  currentRightPWM = slewToTarget(currentRightPWM, targetRightPWM, SLEW_STEP);

  // Левая сторона инвертирована
  driveOneMotor(LEFT_LPWM, LEFT_RPWM, -currentLeftPWM);
  driveOneMotor(RIGHT_LPWM, RIGHT_RPWM, currentRightPWM);

  Serial.print("CH3=");
  Serial.print(chThr);
  Serial.print("\tCH4=");
  Serial.print(chSteer);
  Serial.print("\tCH6=");
  Serial.print(chArm);
  Serial.print("\tL=");
  Serial.print(currentLeftPWM);
  Serial.print("\tR=");
  Serial.println(currentRightPWM);

  delay(20);
}
