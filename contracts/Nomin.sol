/*
-----------------------------------------------------------------
FILE INFORMATION
-----------------------------------------------------------------
file:       Nomin.sol
version:    1.1
author:     Anton Jurisevic
            Mike Spain
            Dominic Romanowski

date:       2018-4-26

checked:    Mike Spain
approved:   Samuel Brooks

-----------------------------------------------------------------
MODULE DESCRIPTION
-----------------------------------------------------------------

Ether-backed nomin stablecoin contract.

This contract issues nomins, which are tokens worth 1 USD each.

Nomins are issuable by Havven holders who have to lock up some
value of their havvens to issue H * Cmax nomins. Where Cmax is
some value less than 1.

A configurable fee is charged on nomin transfers and deposited
into a common pot, which havven holders may withdraw from once per
fee period.

-----------------------------------------------------------------
*/

pragma solidity 0.4.23;


import "contracts/ExternStateFeeToken.sol";
import "contracts/TokenState.sol";
import "contracts/Court.sol";
import "contracts/Havven.sol";


contract Nomin is ExternStateFeeToken {

    /* ========== STATE VARIABLES ========== */

    // The address of the contract which manages confiscation votes.
    Court public court;
    Havven public havven;

    // Accounts which have lost the privilege to transact in nomins.
    mapping(address => bool) public frozen;


    /* ========== CONSTRUCTOR ========== */

    constructor(address _havven, address _owner, TokenState _initialState)
        ExternStateFeeToken("Havven-Backed USD Nomins", "nUSD",
                            15 * UNIT / 10000, // nomin transfers incur a 15 bp fee
                            _havven, // the havven contract is the fee authority
                            _initialState,
                            _owner)
        public
    {
        // It should not be possible to transfer to the nomin contract itself.
        frozen[this] = true;
        havven = Havven(_havven);
    }

    /* ========== SETTERS ========== */

    function setCourt(Court _court)
        external
        onlyOwner
    {
        court = _court;
        emit CourtUpdated(_court);
    }

    function setHavven(Havven _havven)
        external
        onlyOwner
    {
        // havven should be set as the feeAuthority after calling this depending on
        // havven's internal logic
        havven = _havven;
        setFeeAuthority(_havven);
        emit HavvenUpdated(_havven);
    }


    /* ========== MUTATIVE FUNCTIONS ========== */

    /* Override ERC20 transfer function in order to check
     * whether the recipient account is frozen. Note that there is
     * no need to check whether the sender has a frozen account,
     * since their funds have already been confiscated,
     * and no new funds can be transferred to it.*/
    function transfer(address to, uint value)
        public
        returns (bool)
    {
        require(!frozen[to]);
        return super.transfer(to, value);
    }

    /* Override ERC20 transferFrom function in order to check
     * whether the recipient account is frozen. */
    function transferFrom(address from, address to, uint value)
        public
        returns (bool)
    {
        require(!frozen[to]);
        return super.transferFrom(from, to, value);
    }

    /* If a confiscation court motion has passed and reached the confirmation
     * state, the court may transfer the target account's balance to the fee pool
     * and freeze its participation in further transactions. */
    function confiscateBalance(address target)
        external
    {
        // Should be callable only by the confiscation court.
        require(Court(msg.sender) == court);
        
        // A motion must actually be underway.
        uint motionID = court.targetMotionID(target);
        require(motionID != 0);

        // These checks are strictly unnecessary,
        // since they are already checked in the court contract itself.
        require(court.motionConfirming(motionID));
        require(court.motionPasses(motionID));
        require(!frozen[target]);

        // Confiscate the balance in the account and freeze it.
        uint balance = state.balanceOf(target);
        state.setBalanceOf(address(this), safeAdd(state.balanceOf(address(this)), balance));
        state.setBalanceOf(target, 0);
        frozen[target] = true;
        emit AccountFrozen(target, target, balance);
        emit Transfer(target, address(this), balance);
    }

    /* The owner may allow a previously-frozen contract to once
     * again accept and transfer nomins. */
    function unfreezeAccount(address target)
        external
        onlyOwner
    {
        if (frozen[target] && Nomin(target) != this) {
            frozen[target] = false;
            emit AccountUnfrozen(target, target);
        }
    }

    /* Allow havven to burn a certain number of
     * nomins from a target address */
    function burn(address target, uint amount)
        external
        onlyHavven
    {
        state.setBalanceOf(target, safeSub(state.balanceOf(target), amount));
        totalSupply = safeSub(totalSupply, amount);
        emit Transfer(target, address(0), amount);
        emit BurnedNomins(target, amount);
    }

    /* Allow havven to issue a certain number of
     * nomins from a target address */
    function issue(address target, uint amount)
        external
        onlyHavven
    {
        state.setBalanceOf(target, safeAdd(state.balanceOf(target), amount));
        totalSupply = safeAdd(totalSupply, amount);
        emit Transfer(address(0), target, amount);
        emit IssuedNomins(target, amount);
    }

    /* ========== MODIFIERS ========== */

    modifier onlyHavven() {
        require(Havven(msg.sender) == havven);
        _;
    }

    /* ========== EVENTS ========== */

    event CourtUpdated(address newCourt);

    event HavvenUpdated(address havven);

    event AccountFrozen(address target, address indexed targetIndex, uint balance);

    event AccountUnfrozen(address target, address indexed targetIndex);

    event IssuedNomins(address target, uint amount);

    event BurnedNomins(address target, uint amount);
}