// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title Ownable
 * @dev The Ownable contract has an owner address, and provides basic authorization control,
 * a function to transfer ownership to a new address.
 */
contract Ownable {
    address private _owner;

    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    constructor() {
        _transferOwnership(msg.sender);
    }

    /**
     * @dev Returns the address of the current owner.
     */
    function owner() public view virtual returns (address) {
        return _owner;
    }

    /**
     * @dev Throws if called by any account other than the owner.
     */
    modifier onlyOwner() {
        require(owner() == msg.sender, "Ownable: caller is not the owner");
        _;
    }

    /**
     * @dev Transfers ownership of the contract to a new account (`newOwner`).
     * Can only be called by the current owner.
     */
    function transferOwnership(address newOwner) public virtual onlyOwner {
        require(newOwner != address(0), "Ownable: new owner is the zero address");
        _transferOwnership(newOwner);
    }

    /**
     * @dev Transfers ownership of the contract to a new account (`newOwner`).
     * Internal function without access restriction.
     */
    function _transferOwnership(address newOwner) internal virtual {
        address oldOwner = _owner;
        _owner = newOwner;
        emit OwnershipTransferred(oldOwner, newOwner);
    }
}

/**
 * @title ERC20
 * @dev This is a simplified implementation of an ERC20 token.
 */
contract WrappedToken is Ownable {
    mapping(address => uint256) private _balances;

    uint256 private _totalSupply;
    string private _name;
    string private _symbol;
    uint8 private _decimals;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    constructor(string memory name_, string memory symbol_) {
        _name = name_;
        _symbol = symbol_;
        _decimals = 18;
    }

    function name() public view virtual returns (string memory) {
        return _name;
    }

    function symbol() public view virtual returns (string memory) {
        return _symbol;
    }

    function decimals() public view virtual returns (uint8) {
        return _decimals;
    }

    function totalSupply() public view virtual returns (uint256) {
        return _totalSupply;
    }

    function balanceOf(address account) public view virtual returns (uint256) {
        return _balances[account];
    }

    function transfer(address to, uint256 amount) public virtual returns (bool) {
        address owner_ = msg.sender;
        _transfer(owner_, to, amount);
        return true;
    }
    
    // Internal function to handle the transfer logic.
    function _transfer(address from, address to, uint256 amount) internal virtual {
        require(from != address(0), "ERC20: transfer from the zero address");
        require(to != address(0), "ERC20: transfer to the zero address");

        uint256 fromBalance = _balances[from];
        require(fromBalance >= amount, "ERC20: transfer amount exceeds balance");
        unchecked {
            _balances[from] = fromBalance - amount;
        }
        _balances[to] += amount;

        emit Transfer(from, to, amount);
    }

    // Internal function for minting new tokens.
    function _mint(address account, uint256 amount) internal virtual {
        require(account != address(0), "ERC20: mint to the zero address");
        _totalSupply += amount;
        _balances[account] += amount;
        emit Transfer(address(0), account, amount);
    }
}

/**
 * @title Bridge
 * @dev The Bridge contract is responsible for minting wrapped tokens on the EVM chain
 * in response to a lock event on the Minima chain.
 */
contract Bridge is Ownable {
    WrappedToken public wrappedToken;
    
    // A mapping to track that a specific Minima transaction has been processed.
    mapping(bytes32 => bool) public isProcessed;

    constructor(address tokenAddress) {
        wrappedToken = WrappedToken(tokenAddress);
    }

    /**
     * @dev Mints wrapped tokens. This function can only be called by the contract owner (our backend).
     * @param recipient The address on the EVM chain to mint tokens to.
     * @param amount The amount of tokens to mint.
     * @param minimaTxHash The hash of the lock transaction on the Minima chain.
     */
    function mint(address recipient, uint256 amount, bytes32 minimaTxHash) external onlyOwner {
        require(!isProcessed[minimaTxHash], "Bridge: transaction already processed");
        
        // This is where the wrapped token is minted and sent to the recipient.
        wrappedToken._mint(recipient, amount);

        // Mark the Minima transaction as processed to prevent double-spending.
        isProcessed[minimaTxHash] = true;
    }
}
