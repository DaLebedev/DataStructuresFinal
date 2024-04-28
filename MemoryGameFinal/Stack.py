import Card


# Stack data structure represents the deck of memory cards
class Stack:
    def __init__(self, maxSize=36):
        self.maxSize = maxSize
        self.cards = [Card.generateSingleCard() for _ in range(maxSize)]
        self.top = -1

    # Function to check if stack is full
    def isEmpty(self):
        return self.top == -1

    # Function to check if stack is full
    def isFull(self):
        return self.top == self.maxSize - 1

    # Pushes card to top of stack
    def push(self, item):
        if not self.isFull():
            self.top += 1
            self.cards[self.top] = item
        else:
            return "Stack is Full!"

    # Removes and returns the top card in the stack
    def pop(self):
        if not self.isEmpty():
            itemStr = str(self.cards[self.top])
            del self.cards[self.top]
            self.top -= 1
            return itemStr
        else:
            return "Stack is Empty!"

    # Displays top card on stack without removing it
    def peek(self):
        if not self.isEmpty():
            return self.cards[self.top]

    # Displays amount of items in the stack.
    def size(self):
        return self.size

    # Function to print all cards in stack
    def printStack(self):
        if not self.isEmpty():
            stackStr = ""
            for i in range(self.top + 1):
                stackStr += f"{self.cards[i]}, "
            return stackStr
        else:
            return "Stack is Empty!"
