// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IWrappedMinima {
    function mint(address to, uint256 amount) external;
    function burn(address from, uint256 amount) external;
}

contract MinimaBridge {
    address public owner;
    IWrappedMinima public wrappedToken;
    mapping(bytes32 => bool) public processedMinimaTx;

    event BridgedIn(address indexed user, uint256 amount, string minimaAddress, bytes32 minimaTxHash);
    event BridgedOut(address indexed user, uint256 amount);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    constructor(address _wrappedToken) {
        owner = msg.sender;
        wrappedToken = IWrappedMinima(_wrappedToken);
    }

    function bridgeIn(address to, uint256 amount, string calldata minimaAddress, bytes32 minimaTxHash) external onlyOwner {
        require(!processedMinimaTx[minimaTxHash], "Already processed");
        processedMinimaTx[minimaTxHash] = true;
        wrappedToken.mint(to, amount);
        emit BridgedIn(to, amount, minimaAddress, minimaTxHash);
    }

    function bridgeOut(uint256 amount) external {
        wrappedToken.burn(msg.sender, amount);
        emit BridgedOut(msg.sender, amount);
    }

    function transferOwnership(address newOwner) external onlyOwner {
        require(newOwner != address(0), "Zero address");
        owner = newOwner;
    }
}
