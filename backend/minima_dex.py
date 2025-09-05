import json
from typing import Dict, Any

class SimpleDex:
    """
    A simplified DEX (Decentralized Exchange) module using an Automated Market Maker (AMM) model.
    
    This class simulates a liquidity pool and provides functions to swap tokens,
    calculate prices, and add liquidity.
    """

    def __init__(self, token_a_reserve: float, token_b_reserve: float):
        """
        Initializes the DEX with initial liquidity reserves for two tokens.
        
        Args:
            token_a_reserve: The initial reserve amount for Token A.
            token_b_reserve: The initial reserve amount for Token B.
        """
        self.reserves = {
            'tokenA': token_a_reserve,
            'tokenB': token_b_reserve
        }
        self.k = token_a_reserve * token_b_reserve
        print(f"DEX initialized with reserves: {self.reserves}")

    def get_price(self, token_in: str, token_out: str) -> float:
        """
        Calculates the current price (exchange rate) between two tokens.
        
        Args:
            token_in: The token being swapped in.
            token_out: The token being swapped out.
            
        Returns:
            The exchange rate (amount of token_out per 1 unit of token_in).
        """
        if token_in not in self.reserves or token_out not in self.reserves:
            raise ValueError("Invalid token. Must be 'tokenA' or 'tokenB'.")

        return self.reserves[token_out] / self.reserves[token_in]

    def swap_tokens(self, token_in: str, amount_in: float) -> Dict[str, Any]:
        """
        Simulates a token swap and updates the liquidity pool.
        
        Args:
            token_in: The token being swapped in.
            amount_in: The amount of token_in to swap.
            
        Returns:
            A dictionary with the swap result, including the amount received.
        """
        if token_in == 'tokenA':
            token_out = 'tokenB'
        elif token_in == 'tokenB':
            token_out = 'tokenA'
        else:
            raise ValueError("Invalid token. Must be 'tokenA' or 'tokenB'.")

        current_reserve_in = self.reserves[token_in]
        current_reserve_out = self.reserves[token_out]

        # Constant Product Formula: (x + dx) * (y - dy) = k
        new_reserve_in = current_reserve_in + amount_in
        new_reserve_out = self.k / new_reserve_in
        
        amount_out = current_reserve_out - new_reserve_out
        
        # Update reserves
        self.reserves[token_in] = new_reserve_in
        self.reserves[token_out] = new_reserve_out
        
        print(f"Swap executed: {amount_in} {token_in} -> {amount_out} {token_out}")
        print(f"New reserves: {self.reserves}")

        return {
            "status": True,
            "amount_out": amount_out,
            "token_out": token_out
        }

    def add_liquidity(self, amount_a: float, amount_b: float) -> Dict[str, Any]:
        """
        Simulates adding liquidity to the pool.
        
        Args:
            amount_a: Amount of Token A to add.
            amount_b: Amount of Token B to add.
            
        Returns:
            A dictionary with the result of adding liquidity.
        """
        self.reserves['tokenA'] += amount_a
        self.reserves['tokenB'] += amount_b
        self.k = self.reserves['tokenA'] * self.reserves['tokenB']
        
        print(f"Liquidity added: {amount_a} TokenA, {amount_b} TokenB")
        print(f"New reserves: {self.reserves}")
        
        return {
            "status": True,
            "message": "Liquidity added successfully."
        }

# --- Example Usage ---
if __name__ == '__main__':
    # Initialize the DEX with a 1:1 price ratio
    dex = SimpleDex(token_a_reserve=1000, token_b_reserve=1000)

    # Example 1: Get the current price
    print("\n--- Current Price ---")
    current_price = dex.get_price('tokenA', 'tokenB')
    print(f"1 TokenA = {current_price} TokenB")
    
    # Example 2: Perform a swap
    print("\n--- Swapping 50 TokenA ---")
    swap_result = dex.swap_tokens('tokenA', 50)
    print("Swap Result:", swap_result)
    
    # Example 3: Check the new price after the swap
    print("\n--- New Price After Swap ---")
    new_price = dex.get_price('tokenA', 'tokenB')
    print(f"1 TokenA = {new_price} TokenB")

    # Example 4: Add more liquidity to the pool
    print("\n--- Adding Liquidity ---")
    liquidity_result = dex.add_liquidity(100, 100)
    print("Liquidity Result:", liquidity_result)
