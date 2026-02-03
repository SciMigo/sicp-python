# Object-Oriented Programming

## SICP Reference
- Chapter 2.4: Multiple Representations for Abstract Data
- Chapter 2.5: Systems with Generic Operations

## Core Concepts
- Classes as templates for objects
- The `__init__` method and `self`
- Instance variables vs class variables
- Methods as functions bound to objects
- Inheritance: extending and overriding behavior
- Multiple representations via dispatch (type tags, data-directed, message passing)
- Polymorphism and duck typing

## Key Examples (Python)
1. **Account class**: `class Account: def __init__(self, holder, balance=0)` — OOP version of make_account
2. **Inheritance**: `class CheckingAccount(Account)` — adds withdrawal fee
3. **Multiple representations**: Complex numbers in rectangular vs polar form
4. **Dispatch by type**: `isinstance` checks vs method dispatch

## Reference Files
- `2.4-multiple-representations.md`
- `2.5-generic-operations.md`

## Speaker Persona
- Professor Dana: Connects OOP back to message passing and data abstraction
- Alex (student): Sees how classes organize the closure-based patterns from earlier modules
