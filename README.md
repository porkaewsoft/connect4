# connect4

# โปรแกรมเกม Connect 4 ที่ทำงานผ่าน Text Mode กับ AI ที่ใช้ Monte Carlo Tree Search

เกม Connect 4 เป็นเกมสำหรับผู้เล่นสองคน สลับกันหย่อนเหรียญลงในช่องแนวตั้ง โดยหย่อนจากบนลงล่าง ปกติช่องแนวตั้งนี้จะมีจำนวนแปดช่อง เมื่อหย่อนเหรียญลงไปจะทำให้เหรียญไปเรียงซ้อนๆ กันขึ้นไป ซ้อนได้สูงสุด 8 แถว ผู้เล่นทั้งสองคนได้รับเหรียญคนละสี คนไหนที่สามารถทำให้เหรียญของตัวเองสามารถเรียงในแนวตั้ง หรือแนวนอน หรือแนวทะแยงได้ครบสี่เหรียญก่อนถือเป็นผู้ชนะ

สมมติว่า
PLAY1 = 1
PLAY2 = 2

เริ่มเกม 1-8 คือเลขกำกับช่อง เพื่อให้ผู้เล่นป้อน
1 2 3 4 5 6 7 8
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
PLAY 1 : (ป้อนเลขช่องที่ต้องการหย่อนลงไป) สมมติ ป้อน 4

1 2 3 4 5 6 7 8
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0
PLAY 2 : สมมติ ป้อน 5
จะเห็นว่า 1 และ 2 

1 2 3 4 5 6 7 8
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 1 2 0 0 0
สลับกันเล่น เช่นนี้ไปเรื่อยๆ สมมติว่า
เล่นมาถึงตรงนี้ 
1 2 3 4 5 6 7 8
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0
2 1 2 2 1 2 0 0
2 2 1 1 1 2 0 0
2 1 2 1 2 1 0 0
1 2 1 1 2 1 2 0
นั่นแสดงว่าผู้เล่นหมายเลขสองชนะ
เรามาวิเคราะห์โจทย์ปัญหานี้กันว่าจะเขียนโปรแกรมออกมาได้อย่างไร

1.	เราต้องมีพื้นที่เก็บว่าเกมเล่นไปถึงไหนแล้ว ซึ่งก็จะต้องเก็บในตัวแปร สมมติว่า ชื่อ board และมีฟังก์ชั่นแสดงชื่อ showBoard
2.	ต้องมีฟังก์ชั่นที่ตรวจสอบว่ามีผู้เล่นฝ่ายใดฝ่ายหนึ่งชนะแล้วหรือไม่ สมมติ ชื่อ checkWinner
a)	ถ้าผู้เล่น ที่ 1 ชนะ checkWinner = 1
b)	ถ้าผู้เล่น ที่ 2 ชนะ checkWinner = 2
c)	ถ้ายังไม่มีใครชนะเลย ให้ checkWinner = 0
3.	การทำงานจะต้องวนรับค่าจากผู้เล่น 1 และ ผู้เล่น 2 ไปเรื่อยๆ จนกว่าจะมีผู้ชนะ

ทีนี้สมมติว่าเราจะสร้าง AI สำหรับเกมนี้ เราอาจจะใช้ MinMax Algorithm เพื่อหาเส้นทางที่ดีที่สุดก็ได้ แต่วันนี้จะลองมาใช้ Monte Carlo Search Tree กัน

4.	สมมติว่า AI ของเราเป็นผู้เล่นที่ 2 แทนที่เราจะรับค่าจากผู้ใช้ เราจะสร้างฟังก์ชั่นชื่อ MCPlay ขึ้นมาแทน
5.	กระบวนการใน MCPlay ทำอะไรบ้าง
เป้าหมายของ MCPlay คือหาว่าจะลงช่อง 1-8 ช่องไหนดี วิธีการเป็นอย่างไร ลองมาดูๆ กัน 

6.1 จาก Board ปัจจุบัน สมมติลองลงที่ช่องที่ 1
		6.2 จากนั้นสุ่มเลข 1-8 ขึ้นมา 20 ครั้ง
			6.3 1-8 ที่สุ่มมานี้ คือลำดับการเดินของฝ่ายตรงข้าม และฝ่าย AI สลับกับไป ดังนั้นจะได้ Board ในสเตทใหม่ที่เกิดจากการลงตามลำดับนี้
			6.3 ถ้าการเดินนี้ ทำให้ AI ชนะ ให้เพิ่มค่า countWin เพิ่มขึ้น 1
			6.4 ถ้าการเดินนี้ ทำให้ AI แพ้ ให้เพิ่มค่า countLose ขึ้น 1
		6.5 ทำ 6.2-6.4 ซ้ำไปเรื่อยๆ เป็นจำนวน 100 ครั้ง
		6.6 นับจำนวน countWin หารด้วย 100 นี่ก็คือ โอกาสชนะถ้าหาก AI ลงช่องที่ 1 (countLose / 1000) คือ โอกาสแพ้หากลงช่อง 1

6.7 ทำซ้ำกับช่องที่ 2-8 ตาม 6.1-6.6
6.8 ดังนี้แล้วเราจะได้ countWin ของช่องที่ 1-8 ออกมาแล้ว
6.9 การตัดสินใจครั้งสุดท้าย อาจจะเลือกทำได้สองแบบ
		1. เลือก countWin สูงสุด หรือไม่ก็ เลือก countWin-countLose สูงสุด (วิธีนี้เรียกว่า Greedy)
		2. สุ่มแบบ Monte Carlo เอา countWin มาสร้างเป็น distribution แล้วสุ่มอีกครั้งหนึ่ง แบบนี้
				สมมติ countWin รวมกับได้ทั้งหมดคือ 100 เกิดจาก
ช่อง 1-8 ที่มีค่าเป็น 15,10,50,5,5,5,5,5 ตามลำดับ ดังนั้นเราสร้าง array ขึ้นมา 100 ช่องใน array 100 ช่องนี้มีเลข 1 อยู่ 15 ตำแหน่ง เลข 2 อยู่ 10 ตำแหน่ง… ไปเรื่อยๆ 
จากนั้นสุ่มเลขขึ้นมาค่าหนึ่ง สมมติว่า x ถ้า array ตำแหน่งที่ x เป็นเลขอะไร ให้เลขนั้นเป็นคำตอบของ MCPlay
แน่นอนว่าโอกาสจะสุ่มได้เลข 3 มีอยู่มากทีเดียว เพราะมีถึง 50% แต่โอกาสได้เลขอื่นนอกจากเลข 3 ก็มีสัดส่วนไปตามจำนวน countWin
		
ทั้งหมดนี้ก็เป็นการเล่นใน 1 ลูป ซึ่งพอเล่นจบตานี้แล้วก็อาจจะเอาเส้นทางการเล่นนี้มาจำเป็นฐานข้อมูลไว้สำหรับเล่นตาต่อๆ ไปได้ด้วย
