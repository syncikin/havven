from utils.deployutils import MASTER, DUMMY, fresh_account, mine_tx, fast_forward, UNIT

from tests.contract_interfaces.havven_interface import PublicHavvenInterface
from tests.contract_interfaces.nomin_interface import PublicNominInterface
from tests.contract_interfaces.destructible_extern_state_token_interface import DestructibleExternStateTokenInterface
from tests.contract_interfaces.extern_state_fee_token_interface import ExternStateFeeTokenInterface
from tests.contract_interfaces.havven_escrow_interface import PublicHavvenEscrowInterface

#
# class TestProxiedDestructibleExternStateToken(__import__('tests').test_DestructibleExternStateToken.TestDestructibleExternStateToken):
#     @classmethod
#     def setUpClass(cls):
#         cls.proxy, cls.proxied_token, cls.compiled, cls.token_contract, cls.token_abi, cls.token_event_dict, cls.tokenstate = cls.deploy_contracts()
#         cls.token = DestructibleExternStateTokenInterface(cls.proxied_token)
#
#
# class TestProxiedExternStateFeeToken(__import__('tests').test_ExternStateFeeToken.TestExternStateFeeToken):
#     @classmethod
#     def setUpClass(cls):
#
#         cls.compiled, cls.proxy, cls.proxied_feetoken, cls.feetoken_contract, cls.feetoken_event_dict, cls.feestate = cls.deployContracts()
#
#         cls.initial_beneficiary = DUMMY
#         cls.fee_authority = fresh_account()
#
#         cls.feetoken = ExternStateFeeTokenInterface(cls.proxied_feetoken)
#         cls.feetoken.setFeeAuthority(MASTER, cls.fee_authority)
#
#
# class TestProxiedFeeCollection(__import__('tests').test_FeeCollection.TestFeeCollection):
#     @classmethod
#     def setUpClass(cls):
#         cls.havven_proxy, cls.proxied_havven, cls.nomin_proxy, cls.proxied_nomin, cls.havven_contract, cls.nomin_contract, cls.fake_court = cls.deployContracts()
#
#         cls.havven = PublicHavvenInterface(cls.proxied_havven)
#         cls.nomin = PublicNominInterface(cls.proxied_nomin)
#
#         fast_forward(weeks=102)
#
#         cls.fake_court_setNomin = lambda sender, new_nomin: mine_tx(
#             cls.fake_court.functions.setNomin(new_nomin).transact({'from': sender}))
#         cls.fake_court_setConfirming = lambda sender, target, status: mine_tx(
#             cls.fake_court.functions.setConfirming(target, status).transact({'from': sender}))
#         cls.fake_court_setVotePasses = lambda sender, target, status: mine_tx(
#             cls.fake_court.functions.setVotePasses(target, status).transact({'from': sender}))
#         cls.fake_court_confiscateBalance = lambda sender, target: mine_tx(
#             cls.fake_court.functions.confiscateBalance(target).transact({'from': sender}))
#
#         cls.fake_court_setNomin(MASTER, cls.nomin_contract.address)
#
#
# class TestProxiedHavven(__import__('tests').test_Havven.TestHavven):
#     @classmethod
#     def setUpClass(cls):
#         # to avoid overflowing in the negative direction (now - targetFeePeriodDuration * 2)
#         fast_forward(weeks=102)
#
#         cls.havven_proxy, cls.proxied_havven, cls.nomin_proxy, cls.proxied_nomin, \
#             cls.havven_contract, cls.nomin_contract, cls.court_contract, \
#             cls.escrow_contract, cls.construction_block, cls.havven_event_dict = cls.deployContracts()
#
#         cls.havven = PublicHavvenInterface(cls.proxied_havven)
#
#         cls.nomin = PublicNominInterface(cls.proxied_nomin)
#
#         cls.initial_time = cls.havven.lastFeePeriodStartTime()
#         cls.time_fast_forwarded = 0
#
#         cls.base_havven_price = UNIT
#
#
# class TestProxiedHavvenEscrow(__import__('tests').test_HavvenEscrow.TestHavvenEscrow):
#     @classmethod
#     def setUpClass(cls):
#         cls.havven_proxy, cls.proxied_havven, cls.nomin_proxy, cls.proxied_nomin, cls.havven_contract, \
#             cls.nomin_contract, cls.court, cls.escrow_contract, cls.construction_block, \
#             cls.escrow_event_dict = cls.deployContracts()
#         cls.havven = PublicHavvenInterface(cls.havven_contract)
#         cls.nomin = PublicNominInterface(cls.nomin_contract)
#         cls.escrow = PublicHavvenEscrowInterface(cls.escrow_contract)
#

class TestProxiedIssuance(__import__('tests').test_Issuance.TestIssuance):
    @classmethod
    def setUpClass(cls):
        cls.havven_proxy, cls.proxied_havven, cls.nomin_proxy, cls.proxied_nomin, cls.havven_contract, cls.nomin_contract, cls.fake_court, cls.escrow_contract = cls.deployContracts()

        cls.havven = PublicHavvenInterface(cls.havven_contract)
        cls.nomin = PublicNominInterface(cls.nomin_contract)
        cls.escrow = PublicHavvenEscrowInterface(cls.escrow_contract)

        fast_forward(weeks=102)

        cls.fake_court_setNomin = lambda sender, new_nomin: mine_tx(
            cls.fake_court.functions.setNomin(new_nomin).transact({'from': sender}))
        cls.fake_court_setConfirming = lambda sender, target, status: mine_tx(
            cls.fake_court.functions.setConfirming(target, status).transact({'from': sender}))
        cls.fake_court_setVotePasses = lambda sender, target, status: mine_tx(
            cls.fake_court.functions.setVotePasses(target, status).transact({'from': sender}))
        cls.fake_court_confiscateBalance = lambda sender, target: mine_tx(
            cls.fake_court.functions.confiscateBalance(target).transact({'from': sender}))

        cls.fake_court_setNomin(MASTER, cls.nomin_contract.address)