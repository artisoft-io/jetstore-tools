/**
 * JetRule grammar
 */
grammar JetRule;

// The main entry point for parsing a JetRule file.
jetrule: statement* EOF;

statement
  : defineLiteralStmt  
  | defineResourceStmt 
  | lookupTableStmt
  | jetRuleStmt
  | COMMENT            
  ;

// --------------------------------------------------------------------------------------
// Define Literal Statements
// --------------------------------------------------------------------------------------
defineLiteralStmt
  : int32LiteralStmt    
  | uInt32LiteralStmt   
  | int64LiteralStmt    
  | uInt64LiteralStmt   
  | doubleLiteralStmt   
  | stringLiteralStmt   
  ;

int32LiteralStmt:  varType=Int32Type  varName=Identifier ASSIGN declValue=intExpr    SEMICOLON;
uInt32LiteralStmt: varType=UInt32Type varName=Identifier ASSIGN declValue=uintExpr   SEMICOLON;
int64LiteralStmt:  varType=Int64Type  varName=Identifier ASSIGN declValue=intExpr    SEMICOLON;
uInt64LiteralStmt: varType=UInt64Type varName=Identifier ASSIGN declValue=uintExpr   SEMICOLON;
doubleLiteralStmt: varType=DoubleType varName=Identifier ASSIGN declValue=doubleExpr SEMICOLON;
stringLiteralStmt: varType=StringType varName=Identifier ASSIGN declValue=String SEMICOLON;

intExpr
  : '+' intExpr  
  | '-' intExpr  
  | DIGITS
  ;

uintExpr
  : '+' uintExpr
  | DIGITS
  ;

doubleExpr
  : '+' doubleExpr
  | '-' doubleExpr
  | DIGITS ('.' DIGITS)?
  ;

// --------------------------------------------------------------------------------------
// Define Resource Statements
// --------------------------------------------------------------------------------------
defineResourceStmt
  : namedResourceStmt
  | volatileResourceStmt
  ;

namedResourceStmt:    ResourceType         resName=Identifier ASSIGN resCtx=resourceValue SEMICOLON;
volatileResourceStmt: resType=VolatileResourceType resName=Identifier ASSIGN resVal=String SEMICOLON;

resourceValue
  : resVal=NULL
  | resVal=CreateUUIDResource
  | resVal=String
  ;

// --------------------------------------------------------------------------------------
// Define Lookup Table
// --------------------------------------------------------------------------------------
lookupTableStmt: LookupTable lookupName=Identifier '{' 
    COMMENT*
    TableName ':' tblStorageName=Identifier ',' 
    COMMENT*
    Key ':' tblKeys=identifierList ',' 
    COMMENT*
    Columns ':' tblColumns=identifierList 
    COMMENT*
  '}' SEMICOLON;

identifierList: '[' seq=identifierSeq? ']';
identifierSeq: Identifier (',' Identifier)* ;

// --------------------------------------------------------------------------------------
// Define Jet Rule
// --------------------------------------------------------------------------------------
jetRuleStmt: '[' ruleName=Identifier ruleProperties* ']' ':' antecedent+ '->' consequent+ SEMICOLON ;
ruleProperties: ',' key=Identifier ':' valCtx=propertyValue ;
propertyValue: ( val=String | val=TRUE | val=FALSE | intval=intExpr ) ;

antecedent: n=NOT? '(' s=atom p=atom o=atom ')' '.'? ( '[' f=exprTerm ']' )? ;
consequent: '(' s=atom p=atom o=exprTerm ')' '.'? ;

atom
  : '?' Identifier
  | Identifier ':' Identifier
  | Identifier
  ;

exprTerm
  : lhs=exprTerm op=binaryOp rhs=exprTerm          # BinaryExprTerm
  | '(' lhs=exprTerm op=binaryOp rhs=exprTerm ')'  # BinaryExprTerm2
  | op=unaryOp '(' arg=exprTerm ')'                # UnaryExprTerm
  | '(' op=unaryOp arg=exprTerm ')'                # UnaryExprTerm2
  | ident=atom                                     # IdentExprTerm
  | TRUE                                           # TrueExprTerm
  | FALSE                                          # FalseExprTerm
  ;


binaryOp
  : PLUS
  | MINUS
  | MUL
  | DIV
  | OR
  | AND
  ;

unaryOp
  : NOT
  | TOTEXT
  ;

// ======================================================================================
// Lexer section
// --------------------------------------------------------------------------------------
Int32Type: 'int';
UInt32Type: 'uint';
Int64Type: 'long';
UInt64Type: 'ulong';
DoubleType: 'double';
StringType: 'text';

ResourceType: 'resource';
VolatileResourceType: 'volatile_resource';
CreateUUIDResource: 'create_uuid_resource()';

LookupTable: 'lookup_table';
TableName: 'table_name';
Key: 'key';
Columns: 'columns';

TRUE: 'true';
FALSE: 'false';
NOT: 'not';

TOTEXT: 'toText';

PLUS: '+';
MINUS: '-';
MUL: '*';
DIV: '/';
OR: 'or';
AND: 'and';

SEMICOLON: ';';
ASSIGN: '=';
NULL: ('null' | 'NULL' | 'Null');

Identifier:	NONDIGIT (NONDIGIT | DIGITS)*;
fragment NONDIGIT: [a-zA-Z_];
DIGITS: [0-9]+;

// IdentifierList: '[' Identifier* ']';

String: '"' Schar* '"';
fragment Schar: ~ ["\\\r\n] | '\\"' ;

COMMENT: '#' Cchar*;
fragment Cchar: ~ [\r\n];

WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines