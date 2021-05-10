# BASIC-Interpreter
This program uses a subset of BASIC's grammar. The interpreter must is able to receive a parse tree for every line that is scanned and parsed from the program. These parse trees are then evaluated in the interpreter to display the correct output. This output also displays either the correct results or the syntax error followed by the line the error occurred. The interpreter successfully uses the appropriate input files and the program must show the corresponding statements recognized.
- To test a 'BASIC' program, the .bas file must be stored in the 'samples' directory. 
- After running the interpreter, user must type in the program name ('test.bas', etc).

**GRAMMAR USED:**

```

<ID> --> <INT_ID>
| <STRING_ID>
| <FLOAT_ID>
| <BOOL_ID>

<LITERAL> -> <INT_LITERAL>
| <STRING_LITERAL>
| <FLOAT_LITERAL>
| <BOOL_LITERAL>

<REMARK> -> REM

<STATEMENTS> -> <STATEMENT>
| <REMARK>
| <CONDITIONAL>

<CONDITIONAL> -> IF <BOOLEXPR> THEN <STATEMENT>

<STATEMENT> ->
| LET <ID> ‘=’ <EXPR> 
| PRINT (<EXPR> | <BOOLEXPR>){(",", ";") (<EXPR> | <BOOLEXPR>)}
| INPUT <STRING_LITERAL>;<ID> {(",") <ID>}
| INPUT <ID> {(",") <ID>}
| END

<BOOLEXPR> -> <BOOLTERM> {OR <BOOLTERM>}
<BOOLTERM> -> <BOOLFACTOR> {AND <BOOLFACTOR>}
<BOOLFACTOR> -> <BOOL> | NOT(<BOOLEXPR>) | (<BOOLEXPR>)
<BOOL> -> <BOOL_ID> | <BOOL_LITERAL> | <EXPR> (>=  | > | <= | <  | <>) <EXPR>

<EXPR> -->  <TERM> {(+ | -) <TERM>}
<TERM> -> <FACTOR> {(* | /) <FACTOR>}
<FACTOR> -> <ID> | <LITERAL> | (<EXPR>) | INT((<EXPR>))

```
