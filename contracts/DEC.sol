// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

// This contract is a simplified model of a Decentralized Exchange (DEX)
// It is inspired by the constant product market maker formula (x * y = k)
// and handles liquidity provision and token swaps.
contract DEX {
    using SafeERC20 for IERC20;

    // Mapping to hold the reserves of each token in the liquidity pool.
    // token address => token balance
    mapping(address => uint) public reserves;

    // The addresses of the two tokens in the trading pair.
    IERC20 public tokenA;
    IERC20 public tokenB;

    // The total supply of liquidity tokens (LP tokens) that represent a user's share of the pool.
    uint public totalSupply;

    // Mapping to track each user's liquidity tokens (LP tokens).
    // user address => LP token balance
    mapping(address => uint) public liquidity;

    // Events to log key actions.
    event LiquidityAdded(address indexed provider, uint amountA, uint amountB);
    event LiquidityRemoved(address indexed provider, uint amountA, uint amountB);
    event TokensSwapped(address indexed swapper, address fromToken, address toToken, uint amountIn, uint amountOut);

    // Modifier to ensure that a function can only be called with valid token addresses.
    modifier onlyValidTokens(IERC20 _tokenA, IERC20 _tokenB) {
        require(address(_tokenA) != address(0) && address(_tokenB) != address(0), "Invalid token addresses");
        require(address(_tokenA) != address(_tokenB), "Cannot use the same token for both sides");
        tokenA = _tokenA;
        tokenB = _tokenB;
        _;
    }

    constructor(IERC20 _tokenA, IERC20 _tokenB) onlyValidTokens(_tokenA, _tokenB) {}

    // Function to get the current reserves of tokenA and tokenB.
    function getReserves() public view returns (uint, uint) {
        return (reserves[address(tokenA)], reserves[address(tokenB)]);
    }

    // Function to add liquidity to the pool.
    function addLiquidity(uint _amountA, uint _amountB) public {
        require(_amountA > 0 && _amountB > 0, "Amounts must be greater than zero");

        // The contract takes the tokens from the user.
        IERC20(tokenA).safeTransferFrom(msg.sender, address(this), _amountA);
        IERC20(tokenB).safeTransferFrom(msg.sender, address(this), _amountB);

        // Update reserves
        reserves[address(tokenA)] += _amountA;
        reserves[address(tokenB)] += _amountB;

        // Calculate the amount of liquidity tokens (LP tokens) to mint.
        // A simple formula: the square root of the product of amounts.
        uint liquidityMinted;
        if (totalSupply == 0) {
            liquidityMinted = (_amountA * _amountB)**0.5;
        } else {
            // A more complex formula to handle proportional liquidity.
            uint liquidityA = (totalSupply * _amountA) / reserves[address(tokenA)];
            uint liquidityB = (totalSupply * _amountB) / reserves[address(tokenB)];
            liquidityMinted = liquidityA < liquidityB ? liquidityA : liquidityB;
        }

        require(liquidityMinted > 0, "No liquidity minted");

        // Update the total supply of LP tokens and the user's balance.
        totalSupply += liquidityMinted;
        liquidity[msg.sender] += liquidityMinted;

        emit LiquidityAdded(msg.sender, _amountA, _amountB);
    }
    
    // Function to remove liquidity from the pool.
    function removeLiquidity(uint _liquidityAmount) public {
        require(_liquidityAmount > 0, "Amount must be greater than zero");
        require(liquidity[msg.sender] >= _liquidityAmount, "Not enough liquidity tokens");
        
        uint currentTokenA = reserves[address(tokenA)];
        uint currentTokenB = reserves[address(tokenB)];

        // Calculate the amount of tokens to return to the user based on their share of liquidity.
        uint amountA = (currentTokenA * _liquidityAmount) / totalSupply;
        uint amountB = (currentTokenB * _liquidityAmount) / totalSupply;
        
        require(amountA > 0 && amountB > 0, "Amounts to return are zero");

        // Update reserves and user's LP token balance.
        reserves[address(tokenA)] -= amountA;
        reserves[address(tokenB)] -= amountB;
        totalSupply -= _liquidityAmount;
        liquidity[msg.sender] -= _liquidityAmount;
        
        // Transfer the tokens back to the user.
        IERC20(tokenA).safeTransfer(msg.sender, amountA);
        IERC20(tokenB).safeTransfer(msg.sender, amountB);

        emit LiquidityRemoved(msg.sender, amountA, amountB);
    }

    // Function to swap tokens.
    function swapTokens(IERC20 _fromToken, IERC20 _toToken, uint _amountIn) public {
        require(_amountIn > 0, "Amount must be greater than zero");
        require(address(_fromToken) == address(tokenA) || address(_fromToken) == address(tokenB), "Invalid fromToken");
        require(address(_toToken) == address(tokenA) || address(_toToken) == address(tokenB), "Invalid toToken");
        require(address(_fromToken) != address(_toToken), "Cannot swap the same token");

        // The contract takes the tokens from the user.
        _fromToken.safeTransferFrom(msg.sender, address(this), _amountIn);

        // Get reserves of the fromToken and toToken.
        uint reserveIn = reserves[address(_fromToken)];
        uint reserveOut = reserves[address(_toToken)];
        
        // The constant product formula: x * y = k.
        // We use a simplified formula for the output amount.
        uint amountInWithFee = _amountIn * 997;
        uint numerator = amountInWithFee * reserveOut;
        uint denominator = (reserveIn * 1000) + amountInWithFee;
        uint amountOut = numerator / denominator;
        
        require(amountOut > 0, "Insufficient liquidity for this trade");

        // Update reserves after the swap.
        reserves[address(_fromToken)] += _amountIn;
        reserves[address(_toToken)] -= amountOut;

        // Transfer the output tokens to the user.
        _toToken.safeTransfer(msg.sender, amountOut);

        emit TokensSwapped(msg.sender, address(_fromToken), address(_toToken), _amountIn, amountOut);
    }
}

