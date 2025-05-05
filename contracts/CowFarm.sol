// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CowFarm {
    struct Cow {
        uint id;
        address owner;
        address farm;
        bool inFarm;
        uint monthlyFee;
        uint milkCommission;
    }

    uint public cowCounter = 0;
    mapping(uint => Cow) public cows;

    event CowStored(uint cowId, address owner, address farm);
    event MonthlyFeePaid(uint cowId, address farm, uint amount);
    event MilkCommissionPaid(uint cowId, address owner, uint amount);

    function storeCow(address farm, uint monthlyFee, uint milkCommission) public {
        cows[cowCounter] = Cow(cowCounter, msg.sender, farm, true, monthlyFee, milkCommission);
        emit CowStored(cowCounter, msg.sender, farm);
        cowCounter++;
    }

    function payFarm(uint cowId) public payable {
        require(cows[cowId].inFarm, "Cow not in farm");
        require(msg.value == cows[cowId].monthlyFee, "Incorrect fee");
        payable(cows[cowId].farm).transfer(msg.value);
        emit MonthlyFeePaid(cowId, cows[cowId].farm, msg.value);
    }

    function payMilkCommission(uint cowId) public payable {
        require(cows[cowId].inFarm, "Cow not in farm");
        require(msg.value == cows[cowId].milkCommission, "Incorrect commission");
        payable(cows[cowId].owner).transfer(msg.value);
        emit MilkCommissionPaid(cowId, cows[cowId].owner, msg.value);
    }
}
