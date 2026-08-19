"""Lookup table for single-character tokens."""

from gladlang.core.constants.token_types import (
    GL_BIT_NOT,
    GL_COLON,
    GL_COMMA,
    GL_DOT,
    GL_LBRACE,
    GL_LPAREN,
    GL_LSQUARE,
    GL_QMARK,
    GL_RBRACE,
    GL_RPAREN,
    GL_RSQUARE,
    GL_SEMI,
)

SIMPLE_CHARACTER_TOKENS = {
    "(": GL_LPAREN,
    ")": GL_RPAREN,
    ",": GL_COMMA,
    ".": GL_DOT,
    "[": GL_LSQUARE,
    "]": GL_RSQUARE,
    "~": GL_BIT_NOT,
    "{": GL_LBRACE,
    "}": GL_RBRACE,
    ":": GL_COLON,
    "?": GL_QMARK,
    ";": GL_SEMI,
}
