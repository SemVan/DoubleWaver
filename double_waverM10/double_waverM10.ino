#define LED_PIN 13

#define CPU_HZ 48000000
#define TIMER_PRESCALER_DIV 1024

#define CH1_PIN A0
#define CH2_PIN A5

#define ARRAY_SIZE 6000

int current_element = 0;
short channel_1[ARRAY_SIZE];
short channel_2[ARRAY_SIZE];
byte ch1 = CH1_PIN;
byte ch2 = CH2_PIN;
int timer_id;
int m_symbol;

void startTimer(int frequencyHz);
void setTimerFrequency(int frequencyHz);
void TC3_Handler();

bool isLEDOn = false;

void make_measurement() {
  int m_1  = analogRead(ch1);
//  m_1  = analogRead(ch1);
//  m_1  = analogRead(ch1);
  int m_2  = analogRead(ch2);
//  m_2  = analogRead(ch2);
//  m_2  = analogRead(ch2);

  channel_1[current_element] = m_1;
  channel_2[current_element] = m_2;
  current_element++;
  if (current_element == ARRAY_SIZE) {
      NVIC_DisableIRQ(TC3_IRQn);
      send_Data();
  }
  
}


void start_measurement() {
  current_element = 0;
  startTimer(1000);
}


void sendInfo() {
  char message[10] = {'c','o','n','t','a','c','t','y','e','s'};
  for (int i = 0; i<10; i++) {
    SerialUSB.write(message[i]);
  }
  SerialUSB.write(0x0D);
}

void send_Data() {
  for (int i = 0; i<ARRAY_SIZE; i++) {
    SerialUSB.print(channel_1[i]);
    SerialUSB.print('/');
    SerialUSB.print(channel_2[i]);
    SerialUSB.print('|');
  }
  SerialUSB.print("end");
  return;
}

void setup() {
  SerialUSB.begin(115200);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  if(SerialUSB.available()) {
    m_symbol = SerialUSB.read();
    switch(m_symbol) {
     case 'm':
       start_measurement();
       break;
     case 'i':
       sendInfo();
       break;  
     }
  }
 }

void setTimerFrequency(int frequencyHz) {
  int compareValue = (CPU_HZ / (TIMER_PRESCALER_DIV * frequencyHz)) - 1;
  TcCount16* TC = (TcCount16*) TC3;
  // Make sure the count is in a proportional position to where it was
  // to prevent any jitter or disconnect when changing the compare value.
  TC->COUNT.reg = map(TC->COUNT.reg, 0, TC->CC[0].reg, 0, compareValue);
  TC->CC[0].reg = compareValue;
  Serial.println(TC->COUNT.reg);
  Serial.println(TC->CC[0].reg);
  while (TC->STATUS.bit.SYNCBUSY == 1);
}

void startTimer(int frequencyHz) {
  REG_GCLK_CLKCTRL = (uint16_t) (GCLK_CLKCTRL_CLKEN | GCLK_CLKCTRL_GEN_GCLK0 | GCLK_CLKCTRL_ID_TCC2_TC3) ;
  while ( GCLK->STATUS.bit.SYNCBUSY == 1 ); // wait for sync

  TcCount16* TC = (TcCount16*) TC3;

  TC->CTRLA.reg &= ~TC_CTRLA_ENABLE;
  while (TC->STATUS.bit.SYNCBUSY == 1); // wait for sync

  // Use the 16-bit timer
  TC->CTRLA.reg |= TC_CTRLA_MODE_COUNT16;
  while (TC->STATUS.bit.SYNCBUSY == 1); // wait for sync

  // Use match mode so that the timer counter resets when the count matches the compare register
  TC->CTRLA.reg |= TC_CTRLA_WAVEGEN_MFRQ;
  while (TC->STATUS.bit.SYNCBUSY == 1); // wait for sync

  // Set prescaler to 1024
  TC->CTRLA.reg |= TC_CTRLA_PRESCALER_DIV1024;
  while (TC->STATUS.bit.SYNCBUSY == 1); // wait for sync

  setTimerFrequency(frequencyHz);

  // Enable the compare interrupt
  TC->INTENSET.reg = 0;
  TC->INTENSET.bit.MC0 = 1;

  NVIC_EnableIRQ(TC3_IRQn);

  TC->CTRLA.reg |= TC_CTRLA_ENABLE;
  while (TC->STATUS.bit.SYNCBUSY == 1); // wait for sync
}

void TC3_Handler() {
  TcCount16* TC = (TcCount16*) TC3;
  // If this interrupt is due to the compare register matching the timer count
  // we toggle the LED.
  if (TC->INTFLAG.bit.MC0 == 1) {
    TC->INTFLAG.bit.MC0 = 1;
    // Write callback here!!!
//    digitalWrite(LED_PIN, isLEDOn);
//    isLEDOn = !isLEDOn;
    make_measurement();
  }
}
