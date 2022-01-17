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

int32LiteralStmt:  Int32Type  Identifier ASSIGN intExpr    SEMICOLON;
uInt32LiteralStmt: UInt32Type Identifier ASSIGN uintExpr   SEMICOLON;
int64LiteralStmt:  Int64Type  Identifier ASSIGN intExpr    SEMICOLON;
uInt64LiteralStmt: UInt64Type Identifier ASSIGN uintExpr   SEMICOLON;
doubleLiteralStmt: DoubleType Identifier ASSIGN doubleExpr SEMICOLON;
stringLiteralStmt: StringType Identifier ASSIGN String SEMICOLON;

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

namedResourceStmt: ResourceType Identifier ASSIGN resourceValue SEMICOLON;
volatileResourceStmt: VolatileResourceType Identifier ASSIGN String SEMICOLON;

resourceValue
  : NULL
  | CreateUUIDResource
  | String
  ;

// --------------------------------------------------------------------------------------
// Define Lookup Table
// --------------------------------------------------------------------------------------
lookupTableStmt: LookupTable Identifier '{' 
    TableName ':' Identifier ',' COMMENT?
    Key ':' identifierList ',' COMMENT?
    Columns ':' identifierList COMMENT?
  '}' SEMICOLON;

identifierList: '[' identifierSeq? ']';
identifierSeq: Identifier (',' Identifier)* ;

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

PLUS: '+';
MINUS: '-';
SEMICOLON: ';';
ASSIGN: '=';
NULL: ('null' | 'NULL' | 'Null');

Identifier:	NONDIGIT (NONDIGIT | DIGITS)*;
NONDIGIT: [a-zA-Z_];
DIGITS: [0-9]+;

// IdentifierList: '[' Identifier* ']';

String: '"' Schar* '"';
fragment Schar: ~ ["\\\r\n] | '\\"' ;

COMMENT: '#' Cchar*;
fragment Cchar: ~ [\r\n];

WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines