#!/usr/bin/env python3
"""Afaan Oromoo mini-language to Python source-to-source translator.

Usage:
    python translator.py program.yl
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import List, Optional


# -----------------------------
# Tokenizer
# -----------------------------


@dataclass
class Token:
    type: str
    value: str
    line: int
    col: int


KEYWORDS = {
    "haaraa": "NEW",
    "yoo": "IF",
    "yookan": "ELSE",
    "yeroo": "WHILE",
    "hojii": "FUNC",
    "deebi": "RETURN",
    "xumur": "END",
}

BUILTIN_CALL_ALIASES = {
    "maxxansi": "print",
}


class LexError(Exception):
    pass


class ParseError(Exception):
    pass


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.length = len(source)
        self.index = 0
        self.line = 1
        self.col = 1

    def _peek(self) -> str:
        if self.index >= self.length:
            return ""
        return self.source[self.index]

    def _advance(self) -> str:
        ch = self._peek()
        if not ch:
            return ""
        self.index += 1
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def _make_token(self, t: str, value: str, line: int, col: int) -> Token:
        return Token(t, value, line, col)

    def _is_identifier_start(self, ch: str) -> bool:
        return ch == "_" or ch.isalpha()

    def _is_identifier_part(self, ch: str) -> bool:
        return ch == "_" or ch.isalpha() or ch.isdigit()

    def tokens(self) -> List[Token]:
        out: List[Token] = []
        while True:
            ch = self._peek()
            if ch == "":
                out.append(self._make_token("EOF", "", self.line, self.col))
                break

            if ch in " \t\r":
                self._advance()
                continue

            if ch == "\n":
                line, col = self.line, self.col
                self._advance()
                out.append(self._make_token("NEWLINE", "\\n", line, col))
                continue

            if ch == "#":
                while self._peek() not in ("", "\n"):
                    self._advance()
                continue

            if ch.isdigit():
                line, col = self.line, self.col
                val = self._advance()
                while self._peek().isdigit():
                    val += self._advance()
                out.append(self._make_token("NUMBER", val, line, col))
                continue

            if ch in ('"', "'"):
                quote = ch
                line, col = self.line, self.col
                self._advance()
                val = ""
                while True:
                    c = self._peek()
                    if c == "":
                        raise LexError(f"Lakk. {line}: barruun hin cufamne")
                    if c == quote:
                        self._advance()
                        break
                    if c == "\\":
                        self._advance()
                        nxt = self._peek()
                        if nxt == "":
                            raise LexError(f"Lakk. {line}: escape hin guutamne")
                        escapes = {"n": "\n", "t": "\t", '"': '"', "'": "'", "\\": "\\"}
                        val += escapes.get(nxt, nxt)
                        self._advance()
                        continue
                    val += self._advance()
                out.append(self._make_token("STRING", val, line, col))
                continue

            if self._is_identifier_start(ch):
                line, col = self.line, self.col
                val = self._advance()
                while self._is_identifier_part(self._peek()):
                    val += self._advance()
                token_type = KEYWORDS.get(val, "IDENT")
                out.append(self._make_token(token_type, val, line, col))
                continue

            line, col = self.line, self.col

            if ch == "=" and self.index + 1 < self.length and self.source[self.index + 1] == "=":
                self._advance()
                self._advance()
                out.append(self._make_token("EQ", "==", line, col))
                continue

            single = {
                "+": "PLUS",
                "-": "MINUS",
                "*": "STAR",
                "/": "SLASH",
                "(": "LPAREN",
                ")": "RPAREN",
                ",": "COMMA",
                ":": "COLON",
                "<": "LT",
                ">": "GT",
                "=": "ASSIGN",
            }

            if ch in single:
                self._advance()
                out.append(self._make_token(single[ch], ch, line, col))
                continue

            raise LexError(f"Lakk. {line}, Kolomii {col}: mallattoo hin beekamne '{ch}'")

        return out


# -----------------------------
# AST
# -----------------------------


@dataclass
class Program:
    statements: List[Stmt]


class Stmt:
    pass


class Expr:
    pass


@dataclass
class VarDecl(Stmt):
    name: str
    value: Expr


@dataclass
class Assign(Stmt):
    name: str
    value: Expr


@dataclass
class ExprStmt(Stmt):
    expr: Expr


@dataclass
class IfStmt(Stmt):
    condition: Expr
    then_body: List[Stmt]
    else_body: List[Stmt]


@dataclass
class WhileStmt(Stmt):
    condition: Expr
    body: List[Stmt]


@dataclass
class FuncDef(Stmt):
    name: str
    params: List[str]
    body: List[Stmt]


@dataclass
class ReturnStmt(Stmt):
    value: Expr


@dataclass
class Name(Expr):
    value: str


@dataclass
class Number(Expr):
    value: str


@dataclass
class String(Expr):
    value: str


@dataclass
class Binary(Expr):
    left: Expr
    op: str
    right: Expr


@dataclass
class Call(Expr):
    callee: str
    args: List[Expr]


# -----------------------------
# Parser
# -----------------------------


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.index = 0

    def _peek(self) -> Token:
        return self.tokens[self.index]

    def _prev(self) -> Token:
        return self.tokens[self.index - 1]

    def _at_end(self) -> bool:
        return self._peek().type == "EOF"

    def _advance(self) -> Token:
        if not self._at_end():
            self.index += 1
        return self._prev()

    def _check(self, t: str) -> bool:
        return self._peek().type == t

    def _match(self, *types: str) -> bool:
        if self._peek().type in types:
            self._advance()
            return True
        return False

    def _consume(self, t: str, msg: str) -> Token:
        if self._check(t):
            return self._advance()
        tok = self._peek()
        raise ParseError(f"Lakk. {tok.line}, Kolomii {tok.col}: {msg}")

    def _skip_newlines(self) -> None:
        while self._match("NEWLINE"):
            pass

    def parse(self) -> Program:
        statements: List[Stmt] = []
        self._skip_newlines()
        while not self._at_end():
            statements.append(self._statement())
            self._skip_newlines()
        return Program(statements)

    def _statement(self) -> Stmt:
        if self._match("NEW"):
            name = self._consume("IDENT", "Maqaa variable barbaachisa").value
            self._consume("ASSIGN", "'=' barbaachisa")
            value = self._expression()
            return VarDecl(name, value)

        if self._match("IF"):
            condition = self._expression()
            self._consume("COLON", "Erga 'if' booda ':' barbaachisa")
            self._require_newline("If header boodarra sarjaa haaraa barbaachisa")
            then_body = self._block_until({"ELSE", "END"})
            else_body: List[Stmt] = []
            if self._match("ELSE"):
                self._consume("COLON", "Erga 'else' booda ':' barbaachisa")
                self._require_newline("Else boodarra sarjaa haaraa barbaachisa")
                else_body = self._block_until({"END"})
            self._consume("END", "If block xumuruuf 'xumur' barbaachisa")
            return IfStmt(condition, then_body, else_body)

        if self._match("WHILE"):
            condition = self._expression()
            self._consume("COLON", "Erga 'while' booda ':' barbaachisa")
            self._require_newline("While boodarra sarjaa haaraa barbaachisa")
            body = self._block_until({"END"})
            self._consume("END", "While block xumuruuf 'xumur' barbaachisa")
            return WhileStmt(condition, body)

        if self._match("FUNC"):
            name = self._consume("IDENT", "Maqaa hojii barbaachisa").value
            self._consume("LPAREN", "'(' barbaachisa")
            params: List[str] = []
            if not self._check("RPAREN"):
                params.append(self._consume("IDENT", "Maqaa argument barbaachisa").value)
                while self._match("COMMA"):
                    params.append(self._consume("IDENT", "Maqaa argument barbaachisa").value)
            self._consume("RPAREN", "')' barbaachisa")
            self._consume("COLON", "Erga 'hojii' header booda ':' barbaachisa")
            self._require_newline("Function header boodarra sarjaa haaraa barbaachisa")
            body = self._block_until({"END"})
            self._consume("END", "Hojii xumuruuf 'xumur' barbaachisa")
            return FuncDef(name, params, body)

        if self._match("RETURN"):
            val = self._expression()
            return ReturnStmt(val)

        if self._check("IDENT") and self.tokens[self.index + 1].type == "ASSIGN":
            name = self._advance().value
            self._advance()
            value = self._expression()
            return Assign(name, value)

        expr = self._expression()
        return ExprStmt(expr)

    def _require_newline(self, message: str) -> None:
        if not self._match("NEWLINE"):
            tok = self._peek()
            raise ParseError(f"Lakk. {tok.line}, Kolomii {tok.col}: {message}")
        self._skip_newlines()

    def _block_until(self, stop_tokens: set[str]) -> List[Stmt]:
        stmts: List[Stmt] = []
        while not self._at_end() and self._peek().type not in stop_tokens:
            stmts.append(self._statement())
            self._skip_newlines()
        if self._at_end():
            eof = self._peek()
            expected = " or ".join(sorted(stop_tokens))
            raise ParseError(f"Lakk. {eof.line}, Kolomii {eof.col}: block hin cufamne (expected {expected})")
        return stmts

    def _expression(self) -> Expr:
        return self._comparison()

    def _comparison(self) -> Expr:
        expr = self._term()
        while self._match("EQ", "LT", "GT"):
            op = self._prev().value
            right = self._term()
            expr = Binary(expr, op, right)
        return expr

    def _term(self) -> Expr:
        expr = self._factor()
        while self._match("PLUS", "MINUS"):
            op = self._prev().value
            right = self._factor()
            expr = Binary(expr, op, right)
        return expr

    def _factor(self) -> Expr:
        expr = self._unary()
        while self._match("STAR", "SLASH"):
            op = self._prev().value
            right = self._unary()
            expr = Binary(expr, op, right)
        return expr

    def _unary(self) -> Expr:
        if self._match("MINUS"):
            right = self._unary()
            return Binary(Number("0"), "-", right)
        return self._primary()

    def _primary(self) -> Expr:
        if self._match("NUMBER"):
            return Number(self._prev().value)
        if self._match("STRING"):
            return String(self._prev().value)

        if self._match("IDENT"):
            name = self._prev().value
            if self._match("LPAREN"):
                args: List[Expr] = []
                if not self._check("RPAREN"):
                    args.append(self._expression())
                    while self._match("COMMA"):
                        args.append(self._expression())
                self._consume("RPAREN", "')' ያስፈልጋል")
                return Call(name, args)
            return Name(name)

        if self._match("LPAREN"):
            expr = self._expression()
            self._consume("RPAREN", "')' ያስፈልጋል")
            return expr

        tok = self._peek()
        raise ParseError(f"Lakk. {tok.line}, Kolomii {tok.col}: wanti sirrii hin argamne")


# -----------------------------
# Translator
# -----------------------------


class PythonTranslator:
    def __init__(self):
        self.lines: List[str] = []

    def translate(self, program: Program) -> str:
        self.lines = ["# Auto-generated from .yl (Afaan Oromoo language)"]
        for stmt in program.statements:
            self._stmt(stmt, 0)
        return "\n".join(self.lines) + "\n"

    def _emit(self, indent: int, code: str) -> None:
        self.lines.append("    " * indent + code)

    def _stmt(self, stmt: Stmt, indent: int) -> None:
        if isinstance(stmt, VarDecl):
            self._emit(indent, f"{stmt.name} = {self._expr(stmt.value)}")
            return
        if isinstance(stmt, Assign):
            self._emit(indent, f"{stmt.name} = {self._expr(stmt.value)}")
            return
        if isinstance(stmt, ExprStmt):
            self._emit(indent, self._expr(stmt.expr))
            return
        if isinstance(stmt, ReturnStmt):
            self._emit(indent, f"return {self._expr(stmt.value)}")
            return
        if isinstance(stmt, IfStmt):
            self._emit(indent, f"if {self._expr(stmt.condition)}:")
            if stmt.then_body:
                for s in stmt.then_body:
                    self._stmt(s, indent + 1)
            else:
                self._emit(indent + 1, "pass")
            if stmt.else_body:
                self._emit(indent, "else:")
                for s in stmt.else_body:
                    self._stmt(s, indent + 1)
            return
        if isinstance(stmt, WhileStmt):
            self._emit(indent, f"while {self._expr(stmt.condition)}:")
            if stmt.body:
                for s in stmt.body:
                    self._stmt(s, indent + 1)
            else:
                self._emit(indent + 1, "pass")
            return
        if isinstance(stmt, FuncDef):
            params = ", ".join(stmt.params)
            self._emit(indent, f"def {stmt.name}({params}):")
            if stmt.body:
                for s in stmt.body:
                    self._stmt(s, indent + 1)
            else:
                self._emit(indent + 1, "pass")
            return
        raise TypeError(f"Unknown statement type: {type(stmt)}")

    def _expr(self, expr: Expr) -> str:
        if isinstance(expr, Number):
            return expr.value
        if isinstance(expr, String):
            return repr(expr.value)
        if isinstance(expr, Name):
            return expr.value
        if isinstance(expr, Binary):
            return f"({self._expr(expr.left)} {expr.op} {self._expr(expr.right)})"
        if isinstance(expr, Call):
            args = ", ".join(self._expr(a) for a in expr.args)
            callee = BUILTIN_CALL_ALIASES.get(expr.callee, expr.callee)
            return f"{callee}({args})"
        raise TypeError(f"Unknown expression type: {type(expr)}")


def translate_source(source: str) -> str:
    tokens = Lexer(source).tokens()
    program = Parser(tokens).parse()
    return PythonTranslator().translate(program)


def main() -> int:
    if len(sys.argv) != 2:
        print("Fayyadami: python translator.py program.yl")
        return 1

    input_path = sys.argv[1]
    if not os.path.exists(input_path):
        print(f"Faayiliin hin jiru: {input_path}")
        return 1

    if not input_path.lower().endswith(".yl"):
        print("Faayiliin seensa .yl ta'uu qaba")
        return 1

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            src = f.read()
        py_code = translate_source(src)

        out_path = os.path.splitext(input_path)[0] + ".py"
        with open(out_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(py_code)

        print(f"Milkaa'e: {out_path} uume")
        exec(compile(py_code, out_path, "exec"), {"__name__": "__main__"})
        return 0
    except (LexError, ParseError) as e:
        print(f"Dogoggora: {e}")
        return 1
    except Exception as e:
        print(f"Dogoggora hin yaadamne: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
