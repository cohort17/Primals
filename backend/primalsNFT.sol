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
 * @title ERC721
 * @dev This is a simplified implementation of an ERC721 token. It does not
 * include all features of the full standard but provides core functionality
 * for ownership, transfers, and metadata.
 */
contract ERC721 is Ownable {
    // Mapping from token ID to owner address
    mapping(uint256 => address) private _owners;
    
    // Mapping from owner address to a count of their tokens
    mapping(address => uint256) private _balances;

    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);

    /**
     * @dev Returns the number of NFTs in `owner`'s account.
     */
    function balanceOf(address owner) public view returns (uint256) {
        require(owner != address(0), "ERC721: address zero is not a valid owner");
        return _balances[owner];
    }

    /**
     * @dev Returns the owner of the `tokenId` token.
     */
    function ownerOf(uint256 tokenId) public view returns (address) {
        address owner = _owners[tokenId];
        require(owner != address(0), "ERC721: owner query for nonexistent token");
        return owner;
    }

    /**
     * @dev Transfers `tokenId` from `from` to `to`.
     * This is a simplified internal function without full approval logic.
     */
    function _transfer(address from, address to, uint256 tokenId) internal {
        require(ownerOf(tokenId) == from, "ERC721: transfer from incorrect owner");
        require(to != address(0), "ERC721: transfer to the zero address");

        _balances[from] -= 1;
        _balances[to] += 1;
        _owners[tokenId] = to;

        emit Transfer(from, to, tokenId);
    }
    
    /**
     * @dev Mints a token and transfers it to `to`.
     */
    function _mint(address to, uint256 tokenId) internal {
        require(to != address(0), "ERC721: mint to the zero address");
        require(_owners[tokenId] == address(0), "ERC721: token already minted");

        _balances[to] += 1;
        _owners[tokenId] = to;

        emit Transfer(address(0), to, tokenId);
    }
}

/**
 * @title PrimalsNFT
 * @dev This is the main contract for the Primals NFT collection. It inherits from
 * our simplified ERC721 contract and adds a minting function.
 */
contract PrimalsNFT is ERC721 {
    string private _name;
    string private _symbol;
    uint256 private _nextTokenId;

    constructor() {
        _name = "PrimalsNFT";
        _symbol = "PNFT";
        _nextTokenId = 1;
    }
    
    function name() public view returns (string memory) {
        return _name;
    }

    function symbol() public view returns (string memory) {
        return _symbol;
    }

    /**
     * @dev Mints a new NFT to a specified address.
     * This function can only be called by the contract owner.
     * @param to The address of the new owner.
     */
    function mint(address to) external onlyOwner {
        uint256 tokenId = _nextTokenId;
        _mint(to, tokenId);
        _nextTokenId++;
    }
}

