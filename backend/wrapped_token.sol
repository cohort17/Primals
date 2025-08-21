// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

contract WrappedMinimaToken is ERC20, Ownable, Pausable {
    address public bridge;

    constructor() ERC20("WrappedMinima", "wMINIMA") {}

    function setBridge(address _bridge) external onlyOwner {
        require(_bridge != address(0), "Invalid bridge address");
        bridge = _bridge;
    }

    function mint(address to, uint256 amount) external whenNotPaused {
        require(msg.sender == bridge, "Only bridge can mint");
        _mint(to, amount);
    }

    function burn(address from, uint256 amount) external whenNotPaused {
        require(msg.sender == bridge, "Only bridge can burn");
        _burn(from, amount);
    }

    function pause() external onlyOwner {
        _pause();
    }

    function unpause() external onlyOwner {
        _unpause();
    }
}
