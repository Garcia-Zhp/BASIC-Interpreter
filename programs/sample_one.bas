05 REM BASIC boolean operators AND, OR and NOT demo
20 LET A = 3
30 LET B = 7
35 REM the following is not true: because A is smaller than 5
40 IF (A > 5 AND B > 5) THEN PRINT "Both A and B are greater than 5"
45 REM the following is true: because B is greater than 5
50 IF (A > 5 OR B > 5) THEN PRINT "One OF A or B is greater than 5"
55 REM the following is true : because A is not greater than 5
60 IF NOT(A > 5) THEN PRINT "A is not greater than 5"
65 REM the following is not true: because B is greater than 5
70 IF NOT(B > 5) THEN PRINT "B is not greater than 5 #2"
75 REM the following is true: because A is smaller than 5
80 IF NOT(A > 5 AND B > 5) THEN PRINT "Either A or B not greater than 5"
85 REM the following is not true: because B is greater than 5
90 IF NOT(A > 5 OR B > 5) THEN PRINT "Both A and B are smaller or equal than 5"
95 REM the following is identical to line 90
100 IF (A <= 5 AND B <= 5) THEN PRINT "Both A and B are smaller or equal than 5 #2"
105 REM negation of negation gives original statement: true
110 IF NOT(NOT(A < 5)) THEN PRINT "A is smaller than 5"
115 REM the following is identical to line 40. Not true.
120 IF (NOT(A <= 5)) AND (NOT(B <= 5)) THEN PRINT "Both A and B are greater than 5"
125 REM the following condition is always true:
130 IF (A < B) OR (A >= B) THEN PRINT "Always true"
135 REM the following is always false:
140 IF (A < B) AND (A >= B) THEN PRINT "Always false"
145 REM the following is also always true
150 IF (A > B) OR NOT(A > B) THEN PRINT "Always true #2"
155 REM the following is never true:
160 IF (A > B) AND NOT(A > B) THEN PRINT "Always false #2"
170 END

