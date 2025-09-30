from .bank import Bank

"""
Agent Will Use The Bank For
- Minting Notes
- Returning Notes
"""

class Agent:
    def __init__(self, bank: Bank):
        self.bank = bank
        self.wallet = {}

    def withdraw(self):
        serial, note = self.bank.mint()
        self.wallet[serial] = note
        return serial, note
    
    def deposit(self):
        if not self.wallet:
            raise ValueError("Agent wallet is empty")

        serial = next(iter(self.wallet))
        note = self.wallet[serial]

        # Verify with the bank
        result = self.bank.verify(serial, note)

        # Remove from wallet if verified
        if result:
            del self.wallet[serial]
        return serial, result