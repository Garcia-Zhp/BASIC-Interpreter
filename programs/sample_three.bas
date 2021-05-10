05 REM input a number, output its binary representation
30 LET X = 0
40 LET P = 1
50 INPUT "Enter an integer greater or equal than zero: ";A , B , C
80 REM PRINT B
90 LET X = B * P + X
100 LET P = P * 10
110 LET A = (A - B) / 2
130 PRINT "As binary: ";X
140 END