int led = 13;

// Hàm setup chạy một lần duy nhất khi khởi động chương trình
void setup() {                
  // đặt 'led' là OUTPUT
  pinMode(led, OUTPUT);    
}

// Hàm loop chạy mãi mãi sau khi kết thúc hàm setup()
void loop() {
  digitalWrite(led, HIGH);   // bật đèn led sáng
  delay(1000);               // dừng chương trình trong 1 giây => thây đèn sáng được 1 giây
  digitalWrite(led, LOW);    // tắt đèn led
  delay(1000);               // dừng chương trình trong 1 giây => thấy đèn tối được 1 giây
}
