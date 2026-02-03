# Object-Oriented Programming — Slide Outline

## Slide 1: From Functions to Objects
- Recall `make_account(balance)` — state + behavior bundled via closures
- Classes formalize this pattern: state (attributes) + behavior (methods)
- "A class is a blueprint; an object is an instance"

## Slide 2: Defining a Class
- `class Account:` with `__init__(self, holder, balance=0)`
- `self` — the object being created/operated on
- Creating instances: `acc = Account('Alice', 100)`
- Accessing attributes: `acc.holder`, `acc.balance`

## Slide 3: Methods
- `def deposit(self, amount): self.balance += amount; return self.balance`
- `def withdraw(self, amount): ...`
- Methods are functions that receive `self` automatically
- **Checkpoint**: Predict `acc = Account('Bob', 50); acc.deposit(20); acc.withdraw(10); acc.balance` → 60

## Slide 4: Class Variables vs Instance Variables
- Instance: `self.balance` — unique per object
- Class: `interest = 0.02` — shared across all instances
- `Account.interest = 0.05` changes it for all
- `acc.interest = 0.08` creates an instance variable (shadows class)

## Slide 5: Inheritance
- `class CheckingAccount(Account):` — inherits deposit/withdraw
- Override: `def withdraw(self, amount): super().withdraw(amount + 1)` (withdrawal fee)
- New methods: `def write_check(self, amount): ...`
- Inheritance = "is-a" relationship: a CheckingAccount IS an Account

## Slide 6: Method Resolution Order
- `CheckingAccount.withdraw` → look in CheckingAccount first, then Account
- `super()` calls the parent class method
- Environment diagram: instance → class → parent class
- **Checkpoint**: `ch = CheckingAccount('Eve', 100); ch.withdraw(20); ch.balance` → 79 (fee!)

## Slide 7: Multiple Representations
- Problem: complex numbers — rectangular (x + yi) or polar (r, theta)?
- Same operations (`add`, `mul`) work on different representations
- Solution 1: type tags + dispatch table
- Solution 2: classes with shared interface (polymorphism)
- Duck typing: "If it has `add` and `mul`, it's a complex number"

## Slide 8: Connecting the Ideas
- Message passing (module 04) → methods (OOP)
- Closures (module 01) → `__init__` + `self`
- Abstraction barriers (module 04) → class interfaces
- OOP is a design pattern built on the foundations we've learned

## Slide 9: Summary
- Classes organize state and behavior together
- Inheritance enables code reuse and specialization
- Polymorphism: same interface, different implementations
- Preview: Next we'll build an interpreter — and understand how Python itself works
