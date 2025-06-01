// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";

contract MutableCounter is Initializable, OwnableUpgradeable {
    uint256 private _count;
    uint256 private _lastIncrement;
    uint256 private _incrementDelay;
    
    event CountChanged(uint256 newCount, uint256 timestamp);
    event IncrementDelayChanged(uint256 newDelay);
    
    function initialize(uint256 initialCount, uint256 initialDelay) public initializer {
        __Ownable_init();
        _count = initialCount;
        _incrementDelay = initialDelay;
        _lastIncrement = block.timestamp;
    }
    
    function increment() public {
        require(
            block.timestamp >= _lastIncrement + _incrementDelay,
            "Must wait for delay"
        );
        _count += 1;
        _lastIncrement = block.timestamp;
        emit CountChanged(_count, block.timestamp);
    }
    
    function decrement() public onlyOwner {
        require(_count > 0, "Cannot decrement below zero");
        _count -= 1;
        emit CountChanged(_count, block.timestamp);
    }
    
    function setIncrementDelay(uint256 newDelay) public onlyOwner {
        _incrementDelay = newDelay;
        emit IncrementDelayChanged(newDelay);
    }
    
    function getCount() public view returns (uint256) {
        return _count;
    }
    
    function getIncrementDelay() public view returns (uint256) {
        return _incrementDelay;
    }
    
    function getLastIncrement() public view returns (uint256) {
        return _lastIncrement;
    }
} 