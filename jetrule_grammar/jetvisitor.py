import sys
import antlr4 as a4
from py.JetRuleLexer import JetRuleLexer
from py.JetRuleParser import JetRuleParser
from py.JetRuleVisitor import JetRuleVisitor

class JetVisitor(JetRuleVisitor):

  # =====================================================================================
  # Define Literal Statement
  # -------------------------------------------------------------------------------------
  # Visit a parse tree produced by JetRuleParser#defineLiteralStmt.
  def visitDefineLiteralStmt(self, ctx:JetRuleParser.DefineLiteralStmtContext):
    spec = super().visitChildren(ctx)
    print('Literal spec: ',spec)
    return spec

  # Visit a parse tree produced by JetRuleParser#int32LiteralStmt.
  def visitInt32LiteralStmt(self, ctx:JetRuleParser.Int32LiteralStmtContext):
    super().visitChildren(ctx)
    return { 'type': ctx.varType.text, 'id': ctx.varName.text, 'value':  ctx.declValue.getText()}


  # Visit a parse tree produced by JetRuleParser#uInt32LiteralStmt.
  def visitUInt32LiteralStmt(self, ctx:JetRuleParser.UInt32LiteralStmtContext):
    self.visitChildren(ctx)
    return { 'type': ctx.varType.text, 'id': ctx.varName.text, 'value':  ctx.declValue.getText()}


  # Visit a parse tree produced by JetRuleParser#int64LiteralStmt.
  def visitInt64LiteralStmt(self, ctx:JetRuleParser.Int64LiteralStmtContext):
    self.visitChildren(ctx)
    return { 'type': ctx.varType.text, 'id': ctx.varName.text, 'value':  ctx.declValue.getText()}


  # Visit a parse tree produced by JetRuleParser#uInt64LiteralStmt.
  def visitUInt64LiteralStmt(self, ctx:JetRuleParser.UInt64LiteralStmtContext):
    self.visitChildren(ctx)
    return { 'type': ctx.varType.text, 'id': ctx.varName.text, 'value':  ctx.declValue.getText()}


  # Visit a parse tree produced by JetRuleParser#doubleLiteralStmt.
  def visitDoubleLiteralStmt(self, ctx:JetRuleParser.DoubleLiteralStmtContext):
    self.visitChildren(ctx)
    return { 'type': ctx.varType.text, 'id': ctx.varName.text, 'value':  ctx.declValue.getText()}


  # Visit a parse tree produced by JetRuleParser#stringLiteralStmt.
  def visitStringLiteralStmt(self, ctx:JetRuleParser.StringLiteralStmtContext):
    self.visitChildren(ctx)
    return { 'type': ctx.varType.text, 'id': ctx.varName.text, 'value':  ctx.declValue.text}

  # =====================================================================================
  # Define Resource Statement
  # -------------------------------------------------------------------------------------
  # Visit a parse tree produced by JetRuleParser#defineResourceStmt.
  def visitDefineResourceStmt(self, ctx:JetRuleParser.DefineResourceStmtContext):
    spec = super().visitChildren(ctx)
    print('Resource spec: ',spec)
    return spec

  # Visit a parse tree produced by JetRuleParser#namedResourceStmt.
  def visitNamedResourceStmt(self, ctx:JetRuleParser.NamedResourceStmtContext):
    res = super().visitChildren(ctx)
    return { 'type': 'resource', 'id': ctx.resName.text, 'value':  ctx.resCtx.resVal.text}


  # Visit a parse tree produced by JetRuleParser#volatileResourceStmt.
  def visitVolatileResourceStmt(self, ctx:JetRuleParser.VolatileResourceStmtContext):
    super().visitChildren(ctx)
    return { 'type': 'volatile_resource', 'id': ctx.resName.text, 'value': ctx.resVal.text }

  # =====================================================================================
  # Define Resource Statement
  # -------------------------------------------------------------------------------------
  # Visit a parse tree produced by JetRuleParser#lookupTableStmt.
  def visitLookupTableStmt(self, ctx:JetRuleParser.LookupTableStmtContext):
    super().visitChildren(ctx)
    spec = {'name': ctx.lookupName.text, 'table': ctx.tblStorageName.text, 'keys': ctx.tblKeys.seq.getText(), 'columns': ctx.tblColumns.seq.getText()}
    print('Lookup Table spec:', spec)
    return spec

  # =====================================================================================
  # Define Jet Rule Statement
  # -------------------------------------------------------------------------------------
  # Visit a parse tree produced by JetRuleParser#jetRuleStmt.
  def visitJetRuleStmt(self, ctx:JetRuleParser.JetRuleStmtContext):
    super().visitChildren(ctx)
    ruleProperties = ctx.rulePropsCtx.getText() if ctx.rulePropsCtx else None
    spec = {'name': ctx.ruleName.text, 'properties': ruleProperties}
    print('Jet Rule spec:', spec)
    return spec

if __name__ == "__main__":
  
  data =  a4.FileStream('test.jr', encoding='utf-8')
  
  # lexer
  lexer = JetRuleLexer(data)
  stream = a4.CommonTokenStream(lexer)
  
  # parser
  parser = JetRuleParser(stream)
  tree = parser.jetrule()

  # evaluator
  visitor = JetVisitor()
  output = visitor.visit(tree)
  print(output)
