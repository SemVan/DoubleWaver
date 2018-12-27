
#define CH1_PIN A0
#define CH2_PIN A1

#define ARRAY_SIZE 4096

int current_element = 0;
byte ch1 = CH1_PIN;
byte ch2 = CH2_PIN;
int m_symbol;


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
    Serial.print("end");
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
    } else {
      if (byte_in == 'i') {
        Serial.print("contactyes");
      }
    }
  }
} 



