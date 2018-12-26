
#define CH1_PIN A0
#define CH2_PIN A1

#define ARRAY_SIZE 10

int current_element = 0;
int channel_1[ARRAY_SIZE];
int channel_2[ARRAY_SIZE];
byte ch1 = CH1_PIN;
byte ch2 = CH2_PIN;
int timer_id;
int m_symbol;
int toggle1 = 0;


void make_measurement() {
  digitalWrite(8, HIGH);
  int m_1  = analogRead(ch1);
  int m_2  = analogRead(ch2);
  Serial.print(m_1);
  Serial.print('/');
  Serial.print(m_2);
  Serial.print('|');

  current_element++;
  if (current_element == ARRAY_SIZE) {
    disable_timer();
    Serial.print(0x0D);
    current_element = 0; 
  }
  digitalWrite(8, LOW);
}


void set_timer() {
  cli();
  //set timer0 interrupt at 1kHz
  TCCR0A = 0;// set entire TCCR0A register to 0
  TCCR0B = 0;// same for TCCR0B
  TCNT0  = 0;//initialize counter value to 0
  // set compare match register for 2khz increments
  OCR0A = 249;// = (16*10^6) / (2000*64) - 1 (must be <256)
  // turn on CTC mode
  TCCR0A |= (1 << WGM01);
  // Set CS01 and CS00 bits for 64 prescaler
  TCCR0B |= (1 << CS01) | (1 << CS00);   
  // enable timer compare interrupt
  TIMSK0 |= (1 << OCIE0A);
  sei();
}

void disable_timer() {
  TIMSK0 &= ~(1 << OCIE1A);
}

void start_measurement() {
  current_element = 0;
  set_timer();
}


void sendInfo() {
  char message[10] = {'c','o','n','t','a','c','t','y','e','s'};
  for (int i = 0; i<10; i++) {
    Serial.write(message[i]);
  }
  Serial.write(0x0D);
}

void send_Data() {
  for (int i = 0; i<ARRAY_SIZE; i++) {
    send_one_result(channel_1[i]);
    Serial.write(0x7C);
    send_one_result(channel_2[i]);
    Serial.write(0x0D);
  }

  return;
}

void send_one_result(int result) {
  char mask = 0x0F;
  char byteToSend;
  for (int j=0; j<2; j++) {
    for (int i = 0; i<3; i++) {
      byteToSend = (result>>((2-i)*4) & mask);
      if (byteToSend>9) {
        byteToSend = byteToSend + 0x37;
      } else {
        byteToSend = byteToSend + 0x30;
      }
      Serial.write(byteToSend);
    }
  }

  return;
}

ISR(TIMER0_COMPA_vect){
  make_measurement();  
}


void setup() {
  Serial.begin(115200);
  pinMode(8, OUTPUT);
}



void loop() {
  if (Serial.available()>0) {
    int byte_in = Serial.read();
    if (byte_in == 'm') {
      start_measurement();
    } 
  }
} 



