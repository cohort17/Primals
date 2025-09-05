// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

// A simple ERC20 token implementation for demonstration purposes.
// In a real project, you would use existing token contracts.
contract TokenA is ERC20, Ownable {
    constructor() ERC20("Token A", "TKA") Ownable(msg.sender) {
        _mint(msg.sender, 1_000_000 * 10**18);
    }
}

contract TokenB is ERC20, Ownable {
    constructor() ERC20("Token B", "TKB") Ownable(msg.sender) {
        _mint(msg.sender, 1_000_000 * 10**18);
    }
}

contract MinimaDEX is Ownable {
    // Stores the addresses of the two tokens in the liquidity pool.
    address public tokenA;
    address public tokenB;
    
    // An internal constant product invariant (x * y = k).
    uint256 private k;

    // Events to track swaps and liquidity changes.
    event Swap(
        address indexed swapper,
        address indexed tokenIn,
        address indexed tokenOut,
        uint256 amountIn,
        uint256 amountOut
    );

    event LiquidityAdded(
        address indexed provider,
        uint256 amountA,
        uint256 amountB
    );

    constructor(address _tokenA, address _tokenB) Ownable(msg.sender) {
        require(_tokenA != address(0) && _tokenB != address(0), "Invalid token addresses");
        tokenA = _tokenA;
        tokenB = _tokenB;
    }

    // Function to initialize the liquidity pool.
    // Can only be called once by the owner.
    function initializePool(uint256 initialLiquidityA, uint256 initialLiquidityB) external onlyOwner {
        require(k == 0, "Pool already initialized");

        // Transfer initial liquidity from the owner to the contract.
        require(ERC20(tokenA).transferFrom(msg.sender, address(this), initialLiquidityA), "Token A transfer failed");
        require(ERC20(tokenB).transferFrom(msg.sender, address(this), initialLiquidityB), "Token B transfer failed");

        // Calculate the initial invariant.
        k = initialLiquidityA * initialLiquidityB;
        require(k > 0, "Initial liquidity cannot be zero");
    }

    // Swaps `amountIn` of `tokenIn` for `tokenOut`.
    function swap(address tokenIn, uint256 amountIn) external {
        require(tokenIn == tokenA || tokenIn == tokenB, "Invalid token");
        require(k > 0, "Pool not initialized");

        address tokenOut = (tokenIn == tokenA) ? tokenB : tokenA;
        
        // Transfer the input tokens from the user to the contract.
        require(ERC20(tokenIn).transferFrom(msg.sender, address(this), amountIn), "Token transfer failed");

        uint256 reserveIn = ERC20(tokenIn).balanceOf(address(this));
        uint256 reserveOut = ERC20(tokenOut).balanceOf(address(this));

        // Constant product formula to calculate the output amount.
        uint256 amountOut = reserveOut - (k / (reserveIn + amountIn));
        
        // Transfer the output tokens to the user.
        require(ERC20(tokenOut).transfer(msg.sender, amountOut), "Token transfer failed");

        emit Swap(msg.sender, tokenIn, tokenOut, amountIn, amountOut);
    }

    // Adds liquidity to the pool.
    function addLiquidity(uint256 amountA, uint256 amountB) external {
        // Transfer tokens from the user to the contract.
        require(ERC20(tokenA).transferFrom(msg.sender, address(this), amountA), "Token A transfer failed");
        require(ERC20(tokenB).transferFrom(msg.sender, address(this), amountB), "Token B transfer failed");
        
        // Update the constant product invariant.
        uint256 newReserveA = ERC20(tokenA).balanceOf(address(this));
        uint256 newReserveB = ERC20(tokenB).balanceOf(address(this));
        k = newReserveA * newReserveB;

        emit LiquidityAdded(msg.sender, amountA, amountB);
    }
}

