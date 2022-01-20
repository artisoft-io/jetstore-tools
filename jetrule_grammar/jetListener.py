import sys
from typing import Text
import antlr4 as a4
import json
from py.JetRuleLexer import JetRuleLexer
from py.JetRuleParser import JetRuleParser
from py.JetRuleListener import JetRuleListener

class JetListener(JetRuleListener):

  def __init__(self):
    # Define our state model
    self.literals = []
    self.resources = []
    self.lookups = []
    self.jetRules = []

    # Defining intermediate structure for Jet Rule
    self.ruleProps = {}
    self.ruleAntecedents = []

  # Enter a parse tree produced by JetRuleParser#jetrule.
  def enterJetrule(self, ctx:JetRuleParser.JetruleContext):
    print('Starting Visiting Rule File...')

  # Exit a parse tree produced by JetRuleParser#jetrule.
  def exitJetrule(self, ctx:JetRuleParser.JetruleContext):
    print('Finished Visiting Rule File')
    jetRules = {
      'literals': self.literals,
      'resources': self.resources,
      'lookup_tables': self.lookups,
      'jet_rules': self.jetRules
    }
    with open('test.jr.json', 'wt', encoding='utf-8') as f:
        f.write(json.dumps(jetRules, indent=4))

    print('Result saved to test.jr.json')
    # for item in self.literals:
    #   print('    ', item)
    # print()
    # print('Resources:')
    # for item in self.resources:
    #   print('    ', item)
    # print()
    # print('Lookup Tables:')
    # for item in self.lookups:
    #   print('    ', item)
    # print()
    # print('Jet Rules:')
    # for item in self.jetRules:
    #   print('    ', item)
    # print()

  # =====================================================================================
  # Literals
  # -------------------------------------------------------------------------------------
  def exitInt32LiteralStmt(self, ctx:JetRuleParser.Int32LiteralStmtContext):
    self.literals.append({ 'type': ctx.varType.text, 'id': ctx.varName.getText(), 'value':  ctx.declValue.getText()})

  def exitUInt32LiteralStmt(self, ctx:JetRuleParser.UInt32LiteralStmtContext):
    self.literals.append({ 'type': ctx.varType.text, 'id': ctx.varName.getText(), 'value':  ctx.declValue.getText()})

  def exitInt64LiteralStmt(self, ctx:JetRuleParser.Int64LiteralStmtContext):
    self.literals.append({ 'type': ctx.varType.text, 'id': ctx.varName.getText(), 'value':  ctx.declValue.getText()})

  def exitUInt64LiteralStmt(self, ctx:JetRuleParser.UInt64LiteralStmtContext):
    self.literals.append({ 'type': ctx.varType.text, 'id': ctx.varName.getText(), 'value':  ctx.declValue.getText()})

  def exitDoubleLiteralStmt(self, ctx:JetRuleParser.DoubleLiteralStmtContext):
    self.literals.append({ 'type': ctx.varType.text, 'id': ctx.varName.getText(), 'value':  ctx.declValue.getText()})

  def exitStringLiteralStmt(self, ctx:JetRuleParser.StringLiteralStmtContext):
    self.literals.append({ 'type': ctx.varType.text, 'id': ctx.varName.getText(), 'value':  ctx.declValue.text})

  # =====================================================================================
  # Resources
  # -------------------------------------------------------------------------------------
  def exitNamedResourceStmt(self, ctx:JetRuleParser.NamedResourceStmtContext):
    self.resources.append({ 'type': 'resource', 'id': ctx.resName.getText(), 'value':  ctx.resCtx.resVal.text})

  def exitVolatileResourceStmt(self, ctx:JetRuleParser.VolatileResourceStmtContext):
    self.resources.append({ 'type': 'volatile_resource', 'id': ctx.resName.getText(), 'value': ctx.resVal.text })

  # =====================================================================================
  # Lookup Tables
  # -------------------------------------------------------------------------------------
  def exitLookupTableStmt(self, ctx:JetRuleParser.LookupTableStmtContext):
    self.lookups.append({'name': ctx.lookupName.getText(), 'table': ctx.tblStorageName.text, 'keys': ctx.tblKeys.seq.getText(), 'columns': ctx.tblColumns.seq.getText()})

  # =====================================================================================
  # Jet Rules
  # -------------------------------------------------------------------------------------
  # Enter a parse tree produced by JetRuleParser#jetRuleStmt.
  def enterJetRuleStmt(self, ctx:JetRuleParser.JetRuleStmtContext):
    # Entering a Jet Rule
    # Reseting intermediate structure for Jet Rule
    self.ruleProps = {}
    self.ruleAntecedents = []
    self.ruleConsequents = []

  # Exit a parse tree produced by JetRuleParser#jetRuleStmt.
  def exitJetRuleStmt(self, ctx:JetRuleParser.JetRuleStmtContext):
    # Putting the rule together
    self.jetRules.append({'name': ctx.ruleName.text, 
      'properties': self.ruleProps, 
      'antecedents': self.ruleAntecedents,
      'consequents': self.ruleConsequents  })

  # Exit a parse tree produced by JetRuleParser#ruleProperties.
  def exitRuleProperties(self, ctx:JetRuleParser.RulePropertiesContext):
    key = ctx.key.text
    val = ctx.valCtx.val
    val = val.text if val else ctx.valCtx.intval.getText()
    self.ruleProps[key] = val

  # Function to remove the escape \" for resource with name clashing reserved keywords
  def escape(self, str:Text) -> Text:
    if not str:
      return str
    pos1 = str.find(':')
    if pos1>0:
      pos2 = str.find('"')
      if pos2 == pos1+1:
        # print("escape", str, 'to', str.replace('"', ''))
        return str.replace('"', '')
    return str

  # Exit a parse tree produced by JetRuleParser#antecedent.
  def exitAntecedent(self, ctx:JetRuleParser.AntecedentContext):
    subject = self.escape(ctx.s.getText())
    predicate = self.escape(ctx.p.getText())
    self.ruleAntecedents.append({ 'isNot': True if ctx.n else False, 'triple':[subject, predicate, ctx.o.getText()], 'filter': ctx.f.expr if ctx.f else None })

  # Exit a parse tree produced by JetRuleParser#consequent.
  def exitConsequent(self, ctx:JetRuleParser.ConsequentContext):
    subject = self.escape(ctx.s.getText())
    predicate = self.escape(ctx.p.getText())
    self.ruleConsequents.append({ 'triple':[subject, predicate, ctx.o.expr] })

  # Exit a parse tree produced by JetRuleParser#BinaryExprTerm.
  def exitBinaryExprTerm(self, ctx:JetRuleParser.BinaryExprTermContext):
    ctx.expr = {'type': 'binary', 'lhs': ctx.lhs.expr, 'op': ctx.op.getText(), 'rhs': ctx.rhs.expr}

  # Exit a parse tree produced by JetRuleParser#BinaryExprTerm2.
  def exitBinaryExprTerm2(self, ctx:JetRuleParser.BinaryExprTerm2Context):
    ctx.expr = {'type': 'binary', 'lhs': ctx.lhs.expr, 'op': ctx.op.getText(), 'rhs': ctx.rhs.expr}

  # Exit a parse tree produced by JetRuleParser#UnaryExprTerm.
  def exitUnaryExprTerm(self, ctx:JetRuleParser.UnaryExprTermContext):
    ctx.expr = {'type': 'unary', 'arg': ctx.arg.expr, 'op': ctx.op.getText()}

  # Exit a parse tree produced by JetRuleParser#UnaryExprTerm2.
  def exitUnaryExprTerm2(self, ctx:JetRuleParser.UnaryExprTerm2Context):
    ctx.expr = {'type': 'unary', 'arg': ctx.arg.expr, 'op': ctx.op.getText()}

  # Exit a parse tree produced by JetRuleParser#UnaryExprTerm3.
  def exitUnaryExprTerm3(self, ctx:JetRuleParser.UnaryExprTerm3Context):
    ctx.expr = {'type': 'unary', 'arg': ctx.arg.expr, 'op': ctx.op.getText()}

  # Exit a parse tree produced by JetRuleParser#IdentExprTerm.
  def exitIdentExprTerm(self, ctx:JetRuleParser.IdentExprTermContext):
    ident = self.escape(ctx.ident.getText())
    ctx.expr = {'type': 'ident', 'id': ident}

  # Exit a parse tree produced by JetRuleParser#TrueExprTerm.
  def exitTrueExprTerm(self, ctx:JetRuleParser.TrueExprTermContext):
    ctx.expr = {'type': 'keyword', 'id': 'true'}

  # Exit a parse tree produced by JetRuleParser#FalseExprTerm.
  def exitFalseExprTerm(self, ctx:JetRuleParser.FalseExprTermContext):
    ctx.expr = {'type': 'keyword', 'id': 'false'}

if __name__ == "__main__":
  
  data =  a4.FileStream('test.jr', encoding='utf-8')
  
  # lexer
  lexer = JetRuleLexer(data)
  stream = a4.CommonTokenStream(lexer)
  
  # parser
  parser = JetRuleParser(stream)
  tree = parser.jetrule()

  # evaluator
  listener = JetListener()
  walker = a4.ParseTreeWalker()
  walker.walk(listener, tree)
