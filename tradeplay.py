import random
import math


# --- 中央銀行類別 (不變動) ---
class CentralBank:
    def __init__(self, initial_interest_rate=0.03):
        self.market_interest_rate = initial_interest_rate
        self.money_supply_multiplier = 1.0

    def adjust_interest_rate(self, change):
        self.market_interest_rate += change
        self.market_interest_rate = max(0.01, self.market_interest_rate)
        print(f"中央銀行調整了利率，目前市場利率為：{round(self.market_interest_rate * 100, 2)}%。")

    def conduct_qe_qt(self, change_percent):
        self.money_supply_multiplier *= (1 + change_percent)
        print(
            f"中央銀行執行了{'量化寬鬆' if change_percent > 0 else '量化緊縮'}，貨幣供應量變動了 {round(change_percent * 100, 2)}%。")


# --- 房地產類別 (不變動) ---
class Property:
    def __init__(self, name, initial_price, rental_income):
        self.name = name
        self.initial_price = initial_price
        self.price = initial_price
        self.owner = None
        self.rental_income = rental_income
        self.is_mortgaged = False
        self.mortgage_value = initial_price * 0.5
        self.mortgage_interest_rate = 0.10

    def get_mortgage_interest(self):
        return self.mortgage_value * self.mortgage_interest_rate


# --- 新增: 投資顧問服務類別 ---
class AdvisoryService:
    def __init__(self, game):
        self.game = game
        self.history_prices = {
            '科技股': [],
            '比特幣': []
        }

    def update_history_prices(self):
        for asset_name, asset in self.game.assets.items():
            if asset_name in self.history_prices:
                self.history_prices[asset_name].append(asset.price)
                if len(self.history_prices[asset_name]) > 10:
                    self.history_prices[asset_name].pop(0)

    def basic_consultation(self):
        # 簡單趨勢判斷: 過去 3 回合價格變動
        asset_name = random.choice(list(self.history_prices.keys()))
        prices = self.history_prices[asset_name]

        if len(prices) < 3:
            return f"目前缺乏足夠的歷史數據來分析 {asset_name} 市場趨勢，請稍後再試。"

        price_change = prices[-1] - prices[-3]

        if price_change > 0:
            return f"根據我們的初步分析，{asset_name} 市場目前處於**上漲趨勢**，建議持續關注或輕倉做多。"
        elif price_change < 0:
            return f"根據我們的初步分析，{asset_name} 市場目前處於**下跌趨勢**，建議小心謹慎或考慮做空。"
        else:
            return f"根據我們的初步分析，{asset_name} 市場目前處於**盤整階段**，趨勢不明。"

    def advanced_strategy(self):
        # 較複雜策略: 均線交叉判斷
        asset_name = random.choice(list(self.history_prices.keys()))
        prices = self.history_prices[asset_name]

        if len(prices) < 10:
            return f"需要更多歷史數據來進行進階分析，建議等候幾個回合。"

        # 計算短期（5回合）和長期（10回合）移動平均線
        short_ma = sum(prices[-5:]) / 5
        long_ma = sum(prices[-10:]) / 10

        advice = ""
        if short_ma > long_ma and prices[-1] > short_ma:
            advice = f"進階策略建議：{asset_name} 均線呈現**黃金交叉**，當前價格突破短期均線，是**做多**的強烈訊號！"
        elif short_ma < long_ma and prices[-1] < short_ma:
            advice = f"進階策略建議：{asset_name} 均線呈現**死亡交叉**，當前價格跌破短期均線，是**做空**的強烈訊號！"
        else:
            advice = f"進階策略建議：{asset_name} 市場目前趨勢不明顯，建議**觀望**。"

        return advice

    def premium_management(self, player):
        # 頂級服務: 獨家內線與資產調整
        player.has_premium_advisory = True
        player.premium_advisory_turns = 3
        player.premium_advisory_asset = random.choice(list(self.game.assets.keys()))

        # 執行自動資產配置
        print("為您執行自動資產配置中...")
        for stock_name, stock_info in list(player.assets['stocks'].items()):
            current_price = self.game.assets[stock_name].price
            price_change = (current_price - stock_info['price']) / stock_info['price'] if stock_info['price'] > 0 else 0
            if price_change < -0.1:  # 如果虧損超過10%，自動賣出
                total_value = current_price * stock_info['quantity']
                player.cash += total_value
                del player.assets['stocks'][stock_name]
                print(f"  - 您的顧問自動賣出了虧損的 {stock_name}，獲得 {round(total_value, 2)}。")

        # 推薦一個高潛力資產
        best_asset = ""
        max_momentum = -9999
        for asset_name, prices in self.history_prices.items():
            if len(prices) >= 5:
                momentum = prices[-1] - prices[-5]
                if momentum > max_momentum:
                    max_momentum = momentum
                    best_asset = asset_name

        advice = f"頂級顧問消息：在接下來3回合內，我們預計**{player.premium_advisory_asset}**將有非常大的價格波動。建議密切關注！"
        if best_asset:
            advice += f"\n  - 此外，演算法顯示目前**{best_asset}**具有最強的動量，是當前最值得關注的資產。"

        return advice


# --- 玩家類別 (修改) ---
class Player:
    def __init__(self, name, is_human=False):
        self.name = name
        self.cash = 20000
        self.bank_account = 0
        self.assets = {
            'stocks': {},
            'bonds': [],
            'futures': [],
            'options': [],
            'etfs': [],
            'cfds': [],
            'perpetual_contracts': [],
            'trses': [],
            'stablecoins': 0,
            'hedge_fund': False,
            'miner': False,
            'insurance': False
        }
        self.properties = []
        self.debts = {}
        self.mortgaged_properties = []
        self.loans_out = {}
        self.position = 0
        self.is_human = is_human
        self.is_bankrupt = False
        self.fed_card_protection_turns = 0
        self.has_fed_card = False

        # 新增: 投資顧問相關屬性
        self.has_premium_advisory = False
        self.premium_advisory_turns = 0
        self.premium_advisory_asset = None

    def roll_dice(self):
        dice = random.randint(1, 6)
        new_position = self.position + dice

        passed_start = False
        if new_position >= 30:
            passed_start = True

        self.position = new_position % 30
        return dice, passed_start

    def deposit(self, amount, fee):
        if self.cash >= amount + fee:
            self.cash -= (amount + fee)
            self.bank_account += amount
            print(f"{self.name} 成功存入 {amount} 到銀行，並支付了 {fee} 的手續費。")
            return True
        else:
            print("現金不足以完成存款。")
            return False

    def withdraw(self, amount, fee):
        if self.bank_account >= amount:
            self.bank_account -= amount
            self.cash += (amount - fee)
            print(f"{self.name} 成功從銀行提領 {amount}，並支付了 {fee} 的手續費。")
            return True
        else:
            print("存款餘額不足。")
            return False

    def buy_stock(self, stock_name, quantity, price):
        total_cost = quantity * price
        if self.cash >= total_cost:
            self.cash -= total_cost
            if stock_name not in self.assets['stocks']:
                self.assets['stocks'][stock_name] = {'quantity': 0, 'price': price}
            self.assets['stocks'][stock_name]['quantity'] += quantity
            print(f"{self.name} 購買了 {quantity} 份 {stock_name}，花費 {total_cost}。")
            return True
        return False

    def buy_property(self, prop, price):
        if self.cash >= price:
            self.cash -= price
            self.properties.append(prop)
            prop.owner = self
            print(f"{self.name} 成功以 {round(price, 2)} 購買了房產 {prop.name}。")
            return True
        else:
            print(f"{self.name} 現金不足以購買 {prop.name}。")
            return False

    def get_total_assets(self, game_assets):
        worth = self.cash + self.bank_account

        for stock_name, stock_info in self.assets['stocks'].items():
            current_price = game_assets[stock_name].price
            worth += stock_info['quantity'] * current_price

        for prop in self.properties:
            worth += prop.price

        for lender_name, loan in self.debts.items():
            worth -= loan.principal

        for prop in self.mortgaged_properties:
            worth -= prop.mortgage_value

        return worth

    def buy_bond(self, bond):
        if self.cash >= bond.price:
            self.cash -= bond.price
            self.assets['bonds'].append(bond)
            print(f"{self.name} 以 {round(bond.price, 2)} 購買了 {bond.name}。")
        else:
            print(f"{self.name} 現金不足以購買 {bond.name}。")

    def trade_futures(self, asset_name, direction, entry_price, margin, maturity_turns):
        if self.cash >= margin:
            self.cash -= margin
            contract = FuturesContract(asset_name, direction, entry_price, maturity_turns)
            self.assets['futures'].append(contract)
            print(f"{self.name} 以 {round(margin, 2)} 的保證金開立了 {direction} {asset_name} 的期貨合約。")
        else:
            print(f"{self.name} 現金不足以開立期貨合約。")

    def buy_option(self, option_type, asset_name, strike_price, premium, maturity_turns):
        if self.cash >= premium:
            self.cash -= premium
            option = OptionContract(option_type, asset_name, strike_price, premium, maturity_turns)
            self.assets['options'].append(option)
            print(f"{self.name} 以 {round(premium, 2)} 的權利金購買了 {option_type} {asset_name} 的選擇權。")
        else:
            print(f"{self.name} 現金不足以購買選擇權。")

    def buy_etf(self, etf):
        if self.cash >= etf.price:
            self.cash -= etf.price
            self.assets['etfs'].append(etf)
            print(f"{self.name} 以 {etf.price} 購買了 {etf.name}。")
        else:
            print(f"{self.name} 現金不足以購買 ETF。")

    def trade_cfd(self, asset_name, direction, margin, leverage):
        if self.cash >= margin:
            self.cash -= margin
            cfd_contract = CFD(asset_name, direction, margin, leverage)
            self.assets['cfds'].append(cfd_contract)
            print(
                f"{self.name} 以 {round(margin, 2)} 的保證金開立了 {direction} {asset_name} 的 CFD 合約，槓桿為 {leverage} 倍。")
        else:
            print(f"{self.name} 現金不足以開立 CFD 合約。")

    def trade_perpetual(self, asset_name, direction, margin, leverage):
        if self.cash >= margin:
            self.cash -= margin
            contract = PerpetualContract(asset_name, direction, margin, leverage)
            self.assets['perpetual_contracts'].append(contract)
            print(
                f"{self.name} 以 {round(margin, 2)} 的保證金開立了 {direction} {asset_name} 的加密永續合約，槓桿為 {leverage} 倍。")
        else:
            print(f"{self.name} 現金不足以開立加密永續合約。")

    def trade_trs(self, asset_name, direction, notional_value, margin, interest_spread, maturity_turns):
        if self.cash >= margin:
            self.cash -= margin
            contract = TRSContract(asset_name, direction, notional_value, margin, interest_spread, maturity_turns)
            self.assets['trses'].append(contract)
            print(
                f"{self.name} 以 {round(margin, 2)} 的保證金開立了 {direction} {asset_name} 的全回報交換合約，名義本金為 {round(notional_value, 2)}。")
        else:
            print(f"{self.name} 現金不足以開立全回報交換合約。")

    def borrow_loan(self, lender, loan):
        self.cash += loan.principal
        self.debts[lender.name] = loan
        print(f"{self.name} 從 {lender.name} 借款 {loan.principal}，目前現金為 {self.cash}。")

    def repay_loan(self, lender_name):
        loan = self.debts[lender_name]
        total_payment = loan.principal + loan.interest_payment * 5
        if self.cash >= total_payment:
            self.cash -= total_payment
            loan.lender.cash += total_payment
            print(f"{self.name} 提前償還了對 {lender_name} 的貸款，共支付 {round(total_payment, 2)}。")
            del self.debts[lender_name]
            del loan.lender.loans_out[self.name]
        else:
            print(f"{self.name} 的現金不足以償還貸款。")


# --- 金融商品類別 (不變動) ---
class FinancialProduct:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def update_price(self):
        pass


class Stock(FinancialProduct):
    def update_price(self):
        volatility = random.uniform(-0.05, 0.05)
        self.price *= (1 + volatility)
        self.price = round(self.price, 2)


class Cryptocurrency(FinancialProduct):
    def update_price(self):
        volatility = random.uniform(-0.20, 0.20)
        self.price *= (1 + volatility)
        self.price = round(self.price, 2)


class Stablecoin(FinancialProduct):
    def __init__(self, name, price, is_depegged=False):
        super().__init__(name, price)
        self.is_depegged = is_depegged

    def update_price(self):
        if not self.is_depegged:
            self.price = 100
        elif self.price < 100:
            self.price += 1
            if self.price >= 100:
                self.is_depegged = False
                self.price = 100


class Bond(FinancialProduct):
    def __init__(self, name, face_value, coupon_rate, maturity_turns):
        super().__init__(name, face_value)
        self.face_value = face_value
        self.coupon_rate = coupon_rate
        self.maturity_turns = maturity_turns

    def update_price(self, market_interest_rate):
        price_change_factor = (1 + self.coupon_rate) / (1 + market_interest_rate)
        self.price = self.face_value * price_change_factor
        self.price = round(self.price, 2)

    def get_coupon_interest(self):
        if self.maturity_turns > 0:
            return self.face_value * self.coupon_rate / self.maturity_turns
        return 0


class FuturesContract:
    def __init__(self, underlying_asset_name, direction, entry_price, maturity_turns):
        self.underlying_asset_name = underlying_asset_name
        self.direction = direction
        self.entry_price = entry_price
        self.maturity_turns = maturity_turns
        self.value = 0

    def calculate_value(self, current_price):
        if self.direction == "long":
            self.value = (current_price - self.entry_price)
        else:
            self.value = (self.entry_price - current_price)
        return self.value


class OptionContract:
    def __init__(self, option_type, underlying_asset_name, strike_price, premium, maturity_turns):
        self.option_type = option_type
        self.underlying_asset_name = underlying_asset_name
        self.strike_price = strike_price
        self.premium = premium
        self.maturity_turns = maturity_turns

    def get_payoff(self, current_price):
        if self.option_type == 'call':
            return max(0, current_price - self.strike_price)
        else:
            return max(0, self.strike_price - current_price)


class ETF(FinancialProduct):
    def __init__(self, name, underlying_asset_name, price, maturity_turns):
        super().__init__(name, price)
        self.underlying_asset_name = underlying_asset_name
        self.maturity_turns = maturity_turns

    def calculate_value(self, current_underlying_price):
        return self.price


class BufferETF(ETF):
    def __init__(self, name, underlying_asset_name, price, maturity_turns, cap, buffer):
        super().__init__(name, underlying_asset_name, price, maturity_turns)
        self.cap = cap
        self.buffer = buffer
        self.initial_underlying_price = 0

    def calculate_value(self, current_underlying_price):
        if self.initial_underlying_price == 0:
            return self.price

        price_change_rate = (current_underlying_price - self.initial_underlying_price) / self.initial_underlying_price

        if price_change_rate > 0:
            capped_return = min(price_change_rate, self.cap)
            return self.price * (1 + capped_return)
        else:
            buffered_loss = max(0, -price_change_rate - self.buffer)
            return self.price * (1 - buffered_loss)


class AutocallableETF(ETF):
    def __init__(self, name, underlying_asset_name, price, maturity_turns, trigger_price, coupon):
        super().__init__(name, underlying_asset_name, price, maturity_turns)
        self.trigger_price = trigger_price
        self.coupon = coupon
        self.is_redeemed = False

    def check_autocall(self, current_underlying_price):
        if not self.is_redeemed and current_underlying_price >= self.trigger_price:
            self.is_redeemed = True
            return True
        return False

    def get_redemption_value(self):
        return self.price + self.coupon


class CFD:
    def __init__(self, underlying_asset_name, direction, margin, leverage):
        self.underlying_asset_name = underlying_asset_name
        self.direction = direction
        self.margin = margin
        self.leverage = leverage
        self.entry_price = 0
        self.position_size = 0
        self.unrealized_pnl = 0

    def set_entry_price(self, price):
        self.entry_price = price
        self.position_size = self.margin * self.leverage

    def calculate_pnl(self, current_price):
        price_change = current_price - self.entry_price
        if self.direction == "long":
            self.unrealized_pnl = price_change * (self.position_size / self.entry_price)
        else:
            self.unrealized_pnl = -price_change * (self.position_size / self.entry_price)
        return self.unrealized_pnl


class PerpetualContract:
    def __init__(self, underlying_asset_name, direction, margin, leverage):
        self.underlying_asset_name = underlying_asset_name
        self.direction = direction
        self.margin = margin
        self.leverage = leverage
        self.entry_price = 0
        self.position_size = 0
        self.unrealized_pnl = 0

    def set_entry_price(self, price):
        self.entry_price = price
        self.position_size = self.margin * self.leverage

    def calculate_pnl(self, current_price):
        price_change = current_price - self.entry_price
        if self.direction == "long":
            self.unrealized_pnl = price_change * (self.position_size / self.entry_price)
        else:
            self.unrealized_pnl = -price_change * (self.position_size / self.entry_price)
        return self.unrealized_pnl

    def apply_funding_rate(self, funding_rate):
        funding_payment = funding_rate * self.position_size
        if self.direction == "long":
            return -funding_payment
        else:
            return funding_payment


class LoanContract:
    def __init__(self, lender, borrower, principal, interest_rate):
        self.lender = lender
        self.borrower = borrower
        self.principal = principal
        self.interest_rate = interest_rate
        self.is_active = True
        self.interest_payment = self.principal * self.interest_rate


# --- 新增: TRS 合約類別 ---
class TRSContract:
    def __init__(self, underlying_asset_name, direction, notional_value, margin, interest_spread, maturity_turns):
        self.underlying_asset_name = underlying_asset_name
        self.direction = direction
        self.notional_value = notional_value
        self.initial_margin = margin
        self.margin = margin
        self.interest_spread = interest_spread
        self.maturity_turns = maturity_turns
        self.start_price = 0
        self.last_price = 0

    def get_total_return(self, current_price):
        cash_flow = self.notional_value * random.uniform(-0.001, 0.001)
        price_return_rate = (current_price - self.last_price) / self.last_price
        price_return = self.notional_value * price_return_rate
        return price_return + cash_flow

    def get_interest_cost(self, market_interest_rate):
        return self.notional_value * (market_interest_rate + self.interest_spread)


# --- 遊戲主類別 (修改) ---
class FinancialMonopolyGame:
    def __init__(self):
        self.players = [
            Player("你", is_human=True),
            Player("電腦1"),
            Player("電腦2"),
            Player("電腦3")
        ]
        self.central_bank = CentralBank()
        # 新增: 投資顧問NPC
        self.advisory_service = AdvisoryService(self)

        self.assets = {
            "科技股": Stock("科技股", 100),
            "比特幣": Cryptocurrency("比特幣", 50000),
            "穩定幣": Stablecoin("穩定幣", 100)
        }
        self.bonds = {
            "十年期公債": Bond("十年期公債", 10000, 0.05, 10)
        }
        self.properties = [
            Property("台北市信義區豪宅", 100000, 5000),
            Property("台北市大安區店面", 80000, 4000),
            Property("新北市板橋區公寓", 50000, 2500),
            Property("桃園市青埔區別墅", 70000, 3500)
        ]
        # 修改板塊，將期貨交易所改為衍生性商品交易所，並新增投資顧問中心
        self.board = [
            "起點",  # 0
            "股票市場",  # 1
            "機會",  # 2
            "債券市場",  # 3
            self.properties[0],  # 4
            "銀行",  # 5
            "衍生性商品交易所",  # 6
            "命運",  # 7
            self.properties[1],  # 8
            "機會",  # 9
            "房產開發中心",  # 10
            "加密貨幣研究中心",  # 11
            "選擇權交易所",  # 12
            "命運",  # 13
            self.properties[2],  # 14
            "投資顧問中心",  # 15 # 新增板塊
            "差價合約 (CFD)",  # 16
            "機會",  # 17
            self.properties[3],  # 18
            "房產稅務局",  # 19
            "金融高峰會",  # 20
            "股票市場",  # 21
            "命運",  # 22
            "債券市場",  # 23
            "機會",  # 24
            "銀行",  # 25
            "股票市場",  # 26
            "機會",  # 27
            "債券市場",  # 28
            "命運"  # 29
        ]

        self.futures_specs = {
            "科技股": {"margin_rate": 0.1, "maturity_turns": 5},
            "比特幣": {"margin_rate": 0.2, "maturity_turns": 3},
        }
        self.trs_specs = {
            "科技股": {"notional_value_factor": 1.5, "margin_rate": 0.2, "interest_spread": 0.01, "maturity_turns": 5},
            "比特幣": {"notional_value_factor": 1.2, "margin_rate": 0.3, "interest_spread": 0.02, "maturity_turns": 3},
        }
        self.options_specs = {
            "科技股": {"strike_price_factor": 1.1, "maturity_turns": 3},
            "比特幣": {"strike_price_factor": 1.2, "maturity_turns": 2},
        }
        self.etf_specs = {
            "科技股緩衝型ETF": {
                "type": "buffer",
                "underlying_asset": "科技股",
                "price": 1000,
                "maturity_turns": 5,
                "cap": 0.15,
                "buffer": 0.10
            },
            "比特幣自動贖回ETF": {
                "type": "autocallable",
                "underlying_asset": "比特幣",
                "price": 5000,
                "maturity_turns": 3,
                "trigger_price_factor": 1.1,
                "coupon": 1000
            }
        }
        self.cfd_assets = ["科技股", "比特幣"]
        self.crypto_assets = ["比特幣"]
        self.loan_trigger_threshold = 2000
        self.loan_principal = 5000
        self.loan_interest_rate = 0.20
        self.loan_offers = {}
        self.bank_interest_rate = 0.02
        self.bank_fee = 20
        self.turn = 0
        self.round_number = 1
        self.board_size = 30
        self.exclusive_info_turns = {}

    def play_game(self, max_turns_per_round=30):
        while not self.check_game_end_condition():
            print(f"\n{'=' * 40}\n======== 第 {self.round_number} 輪新紀元開始！ ========\n{'=' * 40}")
            for i in range(max_turns_per_round):
                if self.check_game_end_condition():
                    break

                print(f"\n{'*' * 40}\n**** 第 {self.round_number} 輪 - 第 {i + 1} 回合 ****\n{'*' * 40}")
                self.turn += 1

                self.check_special_events()
                self.update_market()
                self.update_property_market()
                self.handle_bank_interest()
                # 新增: 更新投資顧問的歷史價格數據
                self.advisory_service.update_history_prices()

                self.print_player_summary()

                self.check_high_interest_loan_conditions()

                for player in self.players:
                    if not player.is_bankrupt:
                        self.play_turn(player)

                self.handle_loan_payments()
                self.handle_mortgage_payments()
                self.handle_rental_income()

            if not self.check_game_end_condition():
                print("\n===========================\n本回合數已達上限，進入下一個新紀元！\n===========================")
                self.reset_game_board()
                self.round_number += 1

        print("\n==================\n遊戲結束！\n==================")
        self.print_final_summary()

    def check_game_end_condition(self):
        active_players = [p for p in self.players if not p.is_bankrupt]
        if len(active_players) <= 1:
            if len(active_players) == 1:
                print(f"最終贏家是 {active_players[0].name}！")
            else:
                print("所有玩家都破產了，沒有贏家。")
            return True
        return False

    def reset_game_board(self):
        print("\n--- 重置遊戲板塊，所有玩家回到起點 ---")
        for player in self.players:
            if not player.is_bankrupt:
                player.position = 0
                print(f"{player.name} 回到起點。")

    def print_player_summary(self):
        print("\n--- 回合開始：玩家資產總覽 ---")
        stablecoin_price = self.assets["穩定幣"].price
        for player in self.players:
            if not player.is_bankrupt:
                total_assets = player.cash + player.bank_account

                for stock_name, stock_info in player.assets['stocks'].items():
                    current_price = self.assets[stock_name].price
                    total_assets += stock_info['quantity'] * current_price

                for bond in player.assets['bonds']:
                    total_assets += bond.price

                for contract in player.assets['futures']:
                    underlying_asset_name = contract.underlying_asset_name
                    if underlying_asset_name in self.assets:
                        current_price = self.assets[underlying_asset_name].price
                        total_assets += contract.calculate_value(current_price)

                for etf in player.assets['etfs']:
                    if not isinstance(etf, AutocallableETF) or not etf.is_redeemed:
                        if etf.underlying_asset_name in self.assets:
                            current_price = self.assets[etf.underlying_asset_name].price
                            total_assets += etf.calculate_value(current_price)

                for cfd in player.assets['cfds']:
                    if cfd.underlying_asset_name in self.assets:
                        current_price = self.assets[cfd.underlying_asset_name].price
                        total_assets += cfd.margin + cfd.calculate_pnl(current_price)

                for contract in player.assets['perpetual_contracts']:
                    if contract.underlying_asset_name in self.assets:
                        current_price = self.assets[contract.underlying_asset_name].price
                        total_assets += contract.margin + contract.calculate_pnl(current_price)

                for contract in player.assets['trses']:
                    total_assets += contract.margin

                total_assets += player.assets['stablecoins'] * stablecoin_price

                for prop in player.properties:
                    total_assets += prop.price

                for lender_name, loan in player.debts.items():
                    total_assets -= loan.principal

                for prop in player.mortgaged_properties:
                    total_assets -= prop.mortgage_value

                print(
                    f"{player.name}: 現金 {round(player.cash, 2)}, 存款 {round(player.bank_account, 2)}, 總資產 {round(total_assets, 2)}",
                    end='')
                if player.debts:
                    print(f" (負債：{sum(d.principal for d in player.debts.values())})", end='')
                if player.loans_out:
                    print(f" (債權：{sum(l.principal for l in player.loans_out.values())})", end='')
                print()
        print("---------------------------------")

    def update_market(self):
        self.central_bank.adjust_interest_rate(random.uniform(-0.005, 0.005))

        for asset_name, asset in self.assets.items():
            asset.price *= self.central_bank.money_supply_multiplier
            asset.update_price()
            print(f"市場更新：{asset_name} 最新價格為 {round(asset.price, 2)}")

        for bond_name, bond in self.bonds.items():
            bond.update_price(self.central_bank.market_interest_rate)
            print(f"市場更新：{bond_name} 最新價格為 {round(bond.price, 2)}")

        for player in self.players:
            for contract in player.assets['trses']:
                if contract.underlying_asset_name in self.assets:
                    contract.last_price = self.assets[contract.underlying_asset_name].price

    def update_property_market(self):
        property_market_index = random.uniform(0.95, 1.05)
        print(f"房地產市場指數本回合為：{round(property_market_index * 100, 2)}%")
        for prop in self.properties:
            prop.price = prop.initial_price * property_market_index
            prop.price = round(prop.price, 2)
            print(f"房地產更新：{prop.name} 最新價格為 {round(prop.price, 2)}")

    def handle_bank_interest(self):
        print("--- 處理銀行存款利息 ---")
        for player in self.players:
            if player.bank_account > 0:
                interest = player.bank_account * self.bank_interest_rate
                player.bank_account += interest
                print(f"{player.name} 的銀行存款獲得了 {round(interest, 2)} 的利息。")

    def handle_rental_income(self):
        print("--- 處理房產租金收入 ---")
        for player in self.players:
            if not player.is_bankrupt and player.properties:
                total_rental_income = 0
                for prop in player.properties:
                    if not prop.is_mortgaged:
                        total_rental_income += prop.rental_income
                if total_rental_income > 0:
                    player.cash += total_rental_income
                    print(f"{player.name} 本回合獲得了 {round(total_rental_income, 2)} 的房產租金收入。")

    def handle_mortgage_payments(self):
        print("--- 處理房產抵押貸款 ---")
        for player in self.players:
            if not player.is_bankrupt and player.mortgaged_properties:
                for prop in list(player.mortgaged_properties):
                    interest_due = prop.get_mortgage_interest()
                    if player.cash >= interest_due:
                        player.cash -= interest_due
                        print(f"{player.name} 為 {prop.name} 支付了 {round(interest_due, 2)} 的抵押貸款利息。")
                    else:
                        print(f"!!! {player.name} 無法支付 {prop.name} 的抵押貸款利息，銀行沒收了房產！")
                        player.properties.remove(prop)
                        player.mortgaged_properties.remove(prop)
                        prop.owner = None
                        prop.is_mortgaged = False
                        player.is_bankrupt = True
                        break

    def check_special_events(self):
        if random.random() < 0.1:
            print("\n!!! 市場快訊：穩定幣發行商面臨監管調查，穩定幣價值脫鉤！")
            self.assets["穩定幣"].is_depegged = True
            self.assets["穩定幣"].price = random.uniform(90, 99)

        for player in self.players:
            if player.assets['miner']:
                bitcoin_income = random.uniform(100, 500)
                player.cash += bitcoin_income
                print(f"{player.name} 的礦機本回合挖到了 {round(bitcoin_income, 2)} 價值的比特幣。")

            if player.name in self.exclusive_info_turns and self.exclusive_info_turns[player.name] > 0:
                self.exclusive_info_turns[player.name] -= 1
                if random.random() < 0.8:
                    self.provide_exclusive_info(player)

            # 新增: 處理頂級顧問服務的獨家消息
            if player.has_premium_advisory and player.premium_advisory_turns > 0:
                self.handle_premium_advisory_event(player)

    # 新增: 頂級顧問服務的獨家消息處理
    def handle_premium_advisory_event(self, player):
        player.premium_advisory_turns -= 1
        asset_name = player.premium_advisory_asset
        if asset_name in self.assets:
            change_factor = random.uniform(0.1, 0.3)
            # 根據隨機數決定是漲還是跌，並應用到價格上
            if random.random() > 0.5:
                self.assets[asset_name].price *= (1 + change_factor)
                print(
                    f"\n[獨家消息] {player.name} 的顧問消息生效！{asset_name} 價格大漲 {round(change_factor * 100, 2)}%！")
            else:
                self.assets[asset_name].price *= (1 - change_factor)
                print(
                    f"\n[獨家消息] {player.name} 的顧問消息生效！{asset_name} 價格大跌 {round(change_factor * 100, 2)}%！")

        if player.premium_advisory_turns <= 0:
            player.has_premium_advisory = False
            print(f"\n[獨家消息] {player.name} 的頂級顧問服務已到期。")

    def provide_exclusive_info(self, player):
        print(f"\n[專屬資訊] {player.name}，你收到了市場快訊：")
        market_prediction = random.choice(["科技股", "比特幣", "市場利率"])
        if market_prediction == "科技股":
            change = random.uniform(-0.1, 0.1)
            print(f"  - 預計下一回合『科技股』價格將有 {round(change * 100, 2)}% 的變動。")
        elif market_prediction == "比特幣":
            change = random.uniform(-0.2, 0.2)
            print(f"  - 預計下一回合『比特幣』價格將有 {round(change * 100, 2)}% 的變動。")
        elif market_prediction == "市場利率":
            change = random.uniform(-0.005, 0.005)
            print(f"  - 預計下一回合『市場利率』將有 {round(change * 100, 2)}% 的變動。")

    def play_turn(self, player):
        print(f"\n--- 現在是 {player.name} 的回合 ---")

        self.handle_bonds(player)
        self.handle_futures(player)
        self.handle_options(player)
        self.handle_etfs(player)
        self.handle_cfds(player)
        self.handle_perpetual_contracts(player)
        self.handle_trses(player)

        steps, passed_start = player.roll_dice()
        print(f"{player.name} 擲出了 {steps} 點，移動到第 {player.position} 格。")

        if passed_start:
            player.cash += 2000
            print(f"{player.name} 經過起點，獲得 2000 的獎金。")

        self.handle_board_action(player)

        if player.assets['hedge_fund']:
            self.handle_hedge_fund(player)

        if player.cash < 0:
            if player.assets['insurance']:
                recovery_amount = abs(player.cash) * 0.5
                player.cash += recovery_amount
                player.assets['insurance'] = False
                print(f"!!! {player.name} 觸發了市場黑天鵝保險，獲得 {round(recovery_amount, 2)} 補償。保險已失效。")
            else:
                print(f"{player.name} 現金不足，宣告破產！")
                player.is_bankrupt = True

    def check_high_interest_loan_conditions(self):
        self.loan_offers = {}
        for player in self.players:
            if not player.is_bankrupt and not player.debts:
                total_assets = self.calculate_total_assets(player)
                if total_assets < self.loan_trigger_threshold:
                    print(f"\n*** 警告：{player.name} 的資產總額已低於 {self.loan_trigger_threshold}，有破產風險！")
                    self.ask_for_loan(player)

    def ask_for_loan(self, player):
        lenders = [p for p in self.players if p != player and not p.is_bankrupt and p.cash > self.loan_principal]
        if not lenders:
            print("目前沒有玩家有足夠現金可以放款。")
            return

        print(f"『高利貸市場』開啟！")

        lending_player_names = []
        for lender in lenders:
            if lender.is_human:
                choice = input(
                    f"{lender.name}，你是否想以 {self.loan_principal} 的本金向 {player.name} 提供 {self.loan_interest_rate * 100}% 利息的高利貸？(y/n): ").lower()
                if choice == 'y':
                    lending_player_names.append(lender.name)
            else:
                if random.random() > 0.5:
                    lending_player_names.append(lender.name)

        if lending_player_names:
            lender_name = random.choice(lending_player_names)
            lender = next(p for p in self.players if p.name == lender_name)

            loan = LoanContract(lender, player, self.loan_principal, self.loan_interest_rate)
            lender.cash -= self.loan_principal
            player.borrow_loan(lender, loan)
            lender.loans_out[player.name] = loan
        else:
            print(f"{player.name} 尋求高利貸失敗。")

    def handle_loan_payments(self):
        print("\n--- 處理貸款利息支付 ---")
        for player in self.players:
            if not player.is_bankrupt and player.debts:
                for lender_name, loan in list(player.debts.items()):
                    if loan.is_active:
                        interest_due = loan.interest_payment
                        if player.cash >= interest_due:
                            player.cash -= interest_due
                            loan.lender.cash += interest_due
                            print(f"{player.name} 支付了 {lender_name} {round(interest_due, 2)} 的利息。")
                        else:
                            print(f"!!! {player.name} 無法支付給 {lender_name} 的利息，宣告破產！")
                            player.is_bankrupt = True
                            loan.lender.cash += player.cash
                            player.cash = 0
                            loan.is_active = False
                            break

    def calculate_total_assets(self, player):
        return player.get_total_assets(self.assets)

    def handle_bonds(self, player):
        if not player.assets['bonds']:
            return

        bonds_to_remove = []
        for bond in list(player.assets['bonds']):
            if bond.maturity_turns > 0:
                coupon_income = bond.get_coupon_interest()
                player.cash += coupon_income
                print(f"  - 獲得 {round(coupon_income, 2)} 的 {bond.name} 利息收入。")

            bond.maturity_turns -= 1
            if bond.maturity_turns <= 0:
                player.cash += bond.face_value
                print(f"  - {bond.name} 已到期，收回 {bond.face_value} 本金。")
                bonds_to_remove.append(bond)

        for bond in bonds_to_remove:
            player.assets['bonds'].remove(bond)

    def handle_futures(self, player):
        contracts_to_remove = []
        if player.assets['futures']:
            print(f"{player.name} 持有期貨合約，進行每日結算。")

        for contract in list(player.assets['futures']):
            underlying_asset_name = contract.underlying_asset_name
            if underlying_asset_name in self.assets:
                current_price = self.assets[underlying_asset_name].price
                profit_loss = contract.calculate_value(current_price)
                player.cash += profit_loss
                print(
                    f"  - {contract.underlying_asset_name} 期貨合約結算：方向為 {contract.direction}，盈虧為 {round(profit_loss, 2)}。")

                contract.maturity_turns -= 1
                if contract.maturity_turns <= 0:
                    print(f"  - {contract.underlying_asset_name} 期貨合約已到期，平倉。")
                    contracts_to_remove.append(contract)
            else:
                contracts_to_remove.append(contract)

        for contract in contracts_to_remove:
            player.assets['futures'].remove(contract)

    def handle_options(self, player):
        contracts_to_remove = []
        if player.assets['options']:
            print(f"{player.name} 持有選擇權合約，檢查是否到期。")

        for option in list(player.assets['options']):
            option.maturity_turns -= 1
            if option.maturity_turns <= 0:
                underlying_asset_name = option.underlying_asset_name
                if underlying_asset_name in self.assets:
                    current_price = self.assets[underlying_asset_name].price
                    payoff = option.get_payoff(current_price)
                    total_profit = payoff - option.premium
                    player.cash += total_profit
                    print(
                        f"  - {option.underlying_asset_name} {option.option_type} 選擇權已到期，損益為 {round(total_profit, 2)}。")

                contracts_to_remove.append(option)

        for option in contracts_to_remove:
            player.assets['options'].remove(option)

    def handle_etfs(self, player):
        if not player.assets['etfs']:
            return

        etfs_to_remove = []
        print(f"{player.name} 持有 ETF，進行每日檢查。")

        for etf in list(player.assets['etfs']):
            etf.maturity_turns -= 1
            underlying_asset_name = etf.underlying_asset_name
            current_underlying_price = self.assets[underlying_asset_name].price

            if isinstance(etf, AutocallableETF):
                if etf.check_autocall(current_underlying_price):
                    redemption_value = etf.get_redemption_value()
                    player.cash += redemption_value
                    print(f"  - {etf.name} 已觸發自動贖回！獲得 {round(redemption_value, 2)}。")
                    etfs_to_remove.append(etf)

            if etf.maturity_turns <= 0 and not (isinstance(etf, AutocallableETF) and etf.is_redeemed):
                final_value = etf.calculate_value(current_underlying_price)
                player.cash += final_value
                print(f"  - {etf.name} 已到期，最終結算價值為 {round(final_value, 2)}。")
                etfs_to_remove.append(etf)

        for etf in etfs_to_remove:
            player.assets['etfs'].remove(etf)

    def handle_cfds(self, player):
        if not player.assets['cfds']:
            return

        cfds_to_remove = []
        print(f"{player.name} 持有 CFD，進行每日檢查。")

        for cfd in list(player.assets['cfds']):
            if cfd.underlying_asset_name in self.assets:
                current_price = self.assets[cfd.underlying_asset_name].price
                pnl = cfd.calculate_pnl(current_price)

                overnight_cost = cfd.position_size * 0.0001
                player.cash -= overnight_cost
                print(f"  - {cfd.underlying_asset_name} CFD 支付隔夜利息 {round(overnight_cost, 2)}。")

                if player.fed_card_protection_turns > 0:
                    player.fed_card_protection_turns -= 1
                    print(f"  - {player.name} 受到聯準會主席體驗卡保護，本回合免於強制平倉。")
                    continue

                if cfd.margin + pnl < 0.2 * cfd.margin:
                    player.cash += cfd.margin + pnl
                    print(
                        f"  - {cfd.underlying_asset_name} CFD 頭寸因保證金不足被強制平倉！損失 {round(cfd.margin + pnl, 2)}。")
                    cfds_to_remove.append(cfd)

        for cfd in cfds_to_remove:
            player.assets['cfds'].remove(cfd)

    def handle_perpetual_contracts(self, player):
        if not player.assets['perpetual_contracts']:
            return

        contracts_to_remove = []
        print(f"{player.name} 持有加密永續合約，進行每日檢查。")

        for contract in list(player.assets['perpetual_contracts']):
            underlying_asset_name = contract.underlying_asset_name
            if underlying_asset_name in self.assets:
                current_price = self.assets[underlying_asset_name].price
                pnl = contract.calculate_pnl(current_price)

                perpetual_price_offset = random.uniform(-0.01, 0.01) * current_price
                perpetual_price = current_price + perpetual_price_offset

                funding_rate = (perpetual_price - current_price) / current_price * 0.01
                funding_payment = contract.apply_funding_rate(funding_rate)

                player.cash += funding_payment

                if funding_payment > 0:
                    print(f"  - {contract.underlying_asset_name} 永續合約獲得資金費 {round(funding_payment, 2)}。")
                else:
                    print(f"  - {contract.underlying_asset_name} 永續合約支付資金費 {round(-funding_payment, 2)}。")

                if player.fed_card_protection_turns > 0:
                    player.fed_card_protection_turns -= 1
                    print(f"  - {player.name} 受到聯準會主席體驗卡保護，本回合免於強制平倉。")
                    continue

                if contract.margin + pnl < 0.1 * contract.margin:
                    player.cash += contract.margin + pnl
                    print(
                        f"  - {contract.underlying_asset_name} 永續合約因保證金不足被強制平倉！損失 {round(contract.margin + pnl, 2)}。")
                    contracts_to_remove.append(contract)

        for contract in contracts_to_remove:
            player.assets['perpetual_contracts'].remove(contract)

    def handle_trses(self, player):
        if not player.assets['trses']:
            return

        contracts_to_remove = []
        print(f"{player.name} 持有全回報交換 (TRS) 合約，進行每日結算。")

        for contract in list(player.assets['trses']):
            underlying_asset_name = contract.underlying_asset_name
            if underlying_asset_name in self.assets:
                current_price = self.assets[underlying_asset_name].price

                interest_cost = contract.get_interest_cost(self.central_bank.market_interest_rate)
                player.cash -= interest_cost / 10
                print(f"  - {contract.underlying_asset_name} TRS 支付利息成本 {round(interest_cost / 10, 2)}。")

                total_return = contract.get_total_return(current_price)
                if contract.direction == "long":
                    profit_loss = total_return
                else:
                    profit_loss = -total_return

                player.cash += profit_loss
                print(f"  - {contract.underlying_asset_name} TRS 合約盈虧：{round(profit_loss, 2)}。")

                contract.maturity_turns -= 1

                if player.cash < 0:
                    print(f"!!! {player.name} 的現金不足以維持 {contract.underlying_asset_name} TRS 合約，強制平倉！")
                    contracts_to_remove.append(contract)

                if contract.maturity_turns <= 0:
                    print(f"  - {contract.underlying_asset_name} TRS 合約已到期，平倉。")
                    contracts_to_remove.append(contract)
            else:
                contracts_to_remove.append(contract)

        for contract in contracts_to_remove:
            player.assets['trses'].remove(contract)

    def handle_hedge_fund(self, player):
        profit = player.cash * 0.01
        player.cash += profit
        print(f"  - 避險基金本回合帶來了 {round(profit, 2)} 的穩定收益。")

    def handle_bank_transactions(self, player):
        print(f"\n歡迎來到銀行，{player.name}！")
        print(f"您的現金餘額：{round(player.cash, 2)}")
        print(f"您的存款帳戶餘額：{round(player.bank_account, 2)}")
        print(f"目前存款利率：{self.bank_interest_rate * 100}%，每次存提款手續費：{self.bank_fee}")

        if not player.is_human:
            if player.cash > 10000:
                deposit_amount = player.cash - 5000
                if deposit_amount > 0:
                    player.deposit(deposit_amount, self.bank_fee)
            elif player.bank_account > 5000 and player.cash < 2000:
                withdraw_amount = player.bank_account - 2000
                if withdraw_amount > 0:
                    player.withdraw(withdraw_amount, self.bank_fee)
            return

        choice = input("請問您想存錢 (d)、提款 (w) 還是離開 (n)？: ").lower()
        if choice == 'd':
            try:
                amount = float(input("請輸入想存入的金額："))
                player.deposit(amount, self.bank_fee)
            except ValueError:
                print("輸入無效。")
        elif choice == 'w':
            try:
                amount = float(input("請輸入想提領的金額："))
                player.withdraw(amount, self.bank_fee)
            except ValueError:
                print("輸入無效。")
        else:
            print("離開銀行。")

    def handle_property_action(self, player, prop):
        print(f"{player.name} 抵達房地產：{prop.name}，目前價格為 {round(prop.price, 2)}。")
        if prop.owner is None:
            if player.is_human:
                choice = input("此房產無主，是否要購買？(y/n): ").lower()
                if choice == 'y':
                    player.buy_property(prop, prop.price)
            else:
                if player.cash > prop.price * 1.5:
                    player.buy_property(prop, prop.price)
        elif prop.owner == player:
            print("這是你的房產。")
            if player.is_human:
                choice = input("你想要哄抬房價(r)、抵押貸款(m)還是不操作(n)？: ").lower()
                if choice == 'r':
                    cost = prop.price * 0.1
                    if player.cash >= cost:
                        player.cash -= cost
                        prop.price *= 1.2
                        print(f"你花費 {round(cost, 2)} 成功哄抬房價，{prop.name} 價格變為 {round(prop.price, 2)}。")
                    else:
                        print("現金不足以哄抬房價。")
                elif choice == 'm':
                    if not prop.is_mortgaged:
                        player.cash += prop.mortgage_value
                        player.mortgaged_properties.append(prop)
                        prop.is_mortgaged = True
                        print(f"你成功將 {prop.name} 抵押，獲得現金 {round(prop.mortgage_value, 2)}。")
                    else:
                        print("此房產已被抵押。")
            else:
                if random.random() > 0.7:
                    cost = prop.price * 0.1
                    if player.cash >= cost:
                        player.cash -= cost
                        prop.price *= 1.2
                        print(f"電腦玩家 {player.name} 哄抬了房價。")
        else:
            print(f"此房產屬於 {prop.owner.name}。你需要支付租金 {prop.rental_income}。")
            if player.cash >= prop.rental_income:
                player.cash -= prop.rental_income
                prop.owner.cash += prop.rental_income
                print(f"{player.name} 支付了 {round(prop.rental_income, 2)} 租金給 {prop.owner.name}。")

                if player.is_human:
                    choice = input(f"你想要以高於市價的價格收購 {prop.owner.name} 的房產嗎？(y/n): ").lower()
                    if choice == 'y':
                        self.handle_hostile_takeover(player, prop)
            else:
                print(f"{player.name} 現金不足以支付租金，宣告破產！")
                player.is_bankrupt = True

    def handle_hostile_takeover(self, player, prop):
        offer_price = prop.price * 1.2
        print(f"{player.name} 欲以 {round(offer_price, 2)} 收購 {prop.owner.name} 的 {prop.name}。")

        owner = prop.owner
        if not owner.is_human:
            if offer_price > prop.price * 1.5:
                owner.cash += offer_price
                player.cash -= offer_price
                owner.properties.remove(prop)
                player.properties.append(prop)
                prop.owner = player
                print(f"電腦玩家 {owner.name} 接受了收購。")
            else:
                print(f"電腦玩家 {owner.name} 拒絕了收購。")
        else:
            choice = input(
                f"{owner.name}，{player.name} 提出以 {round(offer_price, 2)} 收購你的房產，你是否接受？(y/n): ").lower()
            if choice == 'y':
                owner.cash += offer_price
                player.cash -= offer_price
                owner.properties.remove(prop)
                player.properties.append(prop)
                prop.owner = player
                print(f"{owner.name} 接受了收購。")
            else:
                print(f"{owner.name} 拒絕了收購。")

    def handle_board_action(self, player):
        current_board_item = self.board[player.position]

        if isinstance(current_board_item, Property):
            self.handle_property_action(player, current_board_item)
            return

        action_map = {
            "起點": lambda p: print("通過起點，獲得額外獎勵 2000。"),
            "股票市場": self.show_stock_options,
            "債券市場": self.show_bond_options,
            "銀行": self.handle_bank_transactions,
            "衍生性商品交易所": self.show_derivatives_options,
            "選擇權交易所": self.show_options_options,
            "加密永續合約": self.show_perpetual_options,
            "差價合約 (CFD)": self.show_cfd_options,
            "加密貨幣研究中心": self.show_crypto_center_options,
            "房產開發中心": self.handle_property_development,
            "房產稅務局": self.handle_property_tax,
            "金融高峰會": self.handle_fed_card_event,
            "投資顧問中心": self.handle_advisory_center  # 新增板塊處理
        }

        if current_board_item in action_map:
            action_map[current_board_item](player)
        else:
            print(f"{player.name} 在 {current_board_item} 格子上，沒有特殊事件。")

        if player.is_human and player.debts:
            print("\n你目前有未償還的貸款。")
            lender_name = list(player.debts.keys())[0]
            choice = input(f"是否想償還給 {lender_name} 的高利貸？(y/n): ").lower()
            if choice == 'y':
                player.repay_loan(lender_name)

    # 新增: 處理投資顧問中心板塊
    def handle_advisory_center(self, player):
        print(f"\n歡迎來到『金融智慧顧問中心』，{player.name}！")
        print("我們提供專業的市場分析和投資建議。")
        print("以下是我們的服務列表：")
        print("1. 基礎服務 (趨勢分析) - 費用：2000")
        print("2. 進階服務 (具體交易策略) - 費用：5000")
        print("3. 頂級服務 (獨家內線與資產管理) - 費用：10000 + 總資產2%管理費")

        if not player.is_human:
            self.computer_advisory_strategy(player)
            return

        try:
            choice = input("請輸入您的選擇 (1/2/3, 或 n 離開)：").lower()
            if choice == '1':
                cost = 2000
                if player.cash >= cost:
                    player.cash -= cost
                    advice = self.advisory_service.basic_consultation()
                    print(f"--- 基礎服務顧問報告 ---")
                    print(advice)
                else:
                    print("現金不足，無法購買此服務。")
            elif choice == '2':
                cost = 5000
                if player.cash >= cost:
                    player.cash -= cost
                    advice = self.advisory_service.advanced_strategy()
                    print(f"--- 進階服務顧問報告 ---")
                    print(advice)
                else:
                    print("現金不足，無法購買此服務。")
            elif choice == '3':
                cost = 10000
                management_fee = self.calculate_total_assets(player) * 0.02
                total_cost = cost + management_fee
                if player.cash >= total_cost:
                    player.cash -= total_cost
                    advice = self.advisory_service.premium_management(player)
                    print(f"--- 頂級服務顧問報告 ---")
                    print(advice)
                    print(f"您支付了 {round(cost, 2)} 的服務費和 {round(management_fee, 2)} 的資產管理費。")
                else:
                    print("現金不足，無法購買此服務。")
            else:
                print("離開顧問中心。")
        except ValueError:
            print("輸入無效。")

    # 新增: 電腦玩家顧問策略
    def computer_advisory_strategy(self, player):
        if player.cash > 20000 and random.random() > 0.7:
            choice = random.choice([1, 2, 3])
            if choice == 1 and player.cash >= 2000:
                player.cash -= 2000
                advice = self.advisory_service.basic_consultation()
                print(f"電腦玩家 {player.name} 購買了基礎顧問服務：\n{advice}")
            elif choice == 2 and player.cash >= 5000:
                player.cash -= 5000
                advice = self.advisory_service.advanced_strategy()
                print(f"電腦玩家 {player.name} 購買了進階顧問服務：\n{advice}")
            elif choice == 3 and player.cash >= 10000:
                management_fee = self.calculate_total_assets(player) * 0.02
                if player.cash >= 10000 + management_fee:
                    player.cash -= (10000 + management_fee)
                    advice = self.advisory_service.premium_management(player)
                    print(f"電腦玩家 {player.name} 購買了頂級顧問服務：\n{advice}")
        else:
            print(f"電腦玩家 {player.name} 選擇不使用投資顧問服務。")

    def handle_fed_card_event(self, player):
        print("\n!!! 您來到了『金融高峰會』！")

        if player.has_fed_card:
            print(f"你已經持有聯準會主席體驗卡了。")
            return

        if random.randint(1, 50) == 1:
            print("恭喜！你抽到了極其稀有的『聯準會主席體驗卡』！")

            total_assets = player.get_total_assets(self.assets)
            if total_assets >= 100000000:
                player.has_fed_card = True
                print("你的資產已超過一億元，成功啟動體驗卡！")
                self.execute_fed_card_action(player)
            else:
                print(f"但你的總資產 {round(total_assets, 2)} 未達一億元的啟動門檻，此卡片本局作廢。")
        else:
            print("你參加了高峰會，但沒有特殊事件發生。")

    def execute_fed_card_action(self, player):
        if not player.has_fed_card:
            return

        print("\n[聯準會主席體驗] 請選擇你要執行的權力：")
        print("1. 貨幣政策調整：升息或降息")
        print("2. 量化寬鬆/緊縮：印鈔或縮表")
        print("3. 金融監管干預：提供特殊保護")

        if player.is_human:
            try:
                choice = int(input("請輸入您的選擇 (1/2/3)："))
                if choice == 1:
                    rate_choice = input("你想升息 (h) 還是降息 (l)？: ").lower()
                    if rate_choice == 'h':
                        change = random.uniform(0.01, 0.03)
                        self.central_bank.adjust_interest_rate(change)
                    elif rate_choice == 'l':
                        change = random.uniform(-0.03, -0.01)
                        self.central_bank.adjust_interest_rate(change)
                    else:
                        print("無效選擇，放棄執行。")
                elif choice == 2:
                    money_choice = input("你想量化寬鬆 (qe) 還是量化緊縮 (qt)？: ").lower()
                    if money_choice == 'qe':
                        change_percent = random.uniform(0.03, 0.07)
                        self.central_bank.conduct_qe_qt(change_percent)
                    elif money_choice == 'qt':
                        change_percent = random.uniform(-0.07, -0.03)
                        self.central_bank.conduct_qe_qt(change_percent)
                    else:
                        print("無效選擇，放棄執行。")
                elif choice == 3:
                    protection_choice = input("你想提供強制平倉保護 (p) 還是穩定幣救市 (s)？: ").lower()
                    if protection_choice == 'p':
                        print("你對市場發布了聲明，所有玩家在接下來 3 回合內不會因保證金不足被強制平倉。")
                        for p in self.players:
                            p.fed_card_protection_turns = 3
                    elif protection_choice == 's':
                        if self.assets["穩定幣"].is_depegged:
                            self.assets["穩定幣"].price = 100
                            self.assets["穩定幣"].is_depegged = False
                            self.assets["比特幣"].price *= 1.1
                            print("你對市場發布了穩定幣救市計劃，成功讓穩定幣恢復價值，並刺激了比特幣價格！")
                        else:
                            print("穩定幣目前未脫鉤，此權力無法執行。")
                    else:
                        print("無效選擇，放棄執行。")
            except ValueError:
                print("輸入無效，放棄執行。")
        else:
            self.computer_fed_strategy(player)

        player.has_fed_card = False

    def computer_fed_strategy(self, player):
        print(f"電腦玩家 {player.name} 正在思考如何執行聯準會主席權力...")
        choice = random.randint(1, 3)
        if choice == 1:
            if random.random() > 0.5:
                change = random.uniform(0.01, 0.03)
                self.central_bank.adjust_interest_rate(change)
                print(f"{player.name} 選擇升息。")
            else:
                change = random.uniform(-0.03, -0.01)
                self.central_bank.adjust_interest_rate(change)
                print(f"{player.name} 選擇降息。")
        elif choice == 2:
            if random.random() > 0.5:
                change_percent = random.uniform(0.03, 0.07)
                self.central_bank.conduct_qe_qt(change_percent)
                print(f"{player.name} 選擇量化寬鬆。")
            else:
                change_percent = random.uniform(-0.07, -0.03)
                self.central_bank.conduct_qe_qt(change_percent)
                print(f"{player.name} 選擇量化緊縮。")
        elif choice == 3:
            if self.assets["穩定幣"].is_depegged and random.random() > 0.5:
                self.assets["穩定幣"].price = 100
                self.assets["穩定幣"].is_depegged = False
                self.assets["比特幣"].price *= 1.1
                print(f"{player.name} 選擇穩定幣救市。")
            else:
                for p in self.players:
                    p.fed_card_protection_turns = 3
                print(f"{player.name} 選擇提供強制平倉保護。")

        player.has_fed_card = False

    def handle_property_development(self, player):
        print(f"歡迎來到房產開發中心，{player.name}！")
        if not player.properties:
            print("你沒有任何房產可以開發。")
            return

        print("你擁有的房產：")
        for i, prop in enumerate(player.properties):
            print(f"{i + 1}. {prop.name} (目前租金: {prop.rental_income})")

        if player.is_human:
            try:
                choice = int(input("請選擇要開發的房產 (輸入編號，或 0 離開)："))
                if 1 <= choice <= len(player.properties):
                    prop = player.properties[choice - 1]
                    cost = prop.price * 0.1
                    if player.cash >= cost:
                        player.cash -= cost
                        prop.rental_income *= 1.5
                        print(
                            f"你花費 {round(cost, 2)} 成功開發 {prop.name}，租金收入提升至 {round(prop.rental_income, 2)}。")
                    else:
                        print("現金不足以支付開發費用。")
            except ValueError:
                print("輸入無效。")
        else:
            prop = random.choice(player.properties)
            cost = prop.price * 0.1
            if player.cash >= cost:
                player.cash -= cost
                prop.rental_income *= 1.5
                print(f"電腦玩家 {player.name} 成功開發了房產 {prop.name}。")

    def handle_property_tax(self, player):
        print(f"歡迎來到房產稅務局，{player.name}！")
        if not player.properties:
            print("你沒有任何房產，無需繳稅。")
            return

        tax_rate = 0.05
        total_property_value = sum(p.price for p in player.properties)
        tax_due = total_property_value * tax_rate

        if player.cash >= tax_due:
            player.cash -= tax_due
            print(f"你擁有總價值 {round(total_property_value, 2)} 的房產，需要繳納 {round(tax_due, 2)} 的房產稅。")
        else:
            print(f"你無法繳納 {round(tax_due, 2)} 的房產稅，宣告破產！")
            player.is_bankrupt = True

    def get_option_premium(self, option_type, current_price, strike_price, maturity_turns):
        intrinsic_value = 0
        if option_type == 'call':
            intrinsic_value = max(0, current_price - strike_price)
        else:
            intrinsic_value = max(0, strike_price - current_price)

        time_value_factor = 0.05
        time_value = maturity_turns * time_value_factor * current_price

        return intrinsic_value + time_value

    def show_stock_options(self, player):
        print(f"{player.name} 抵達『股票市場』！")
        stock_name, stock = list(self.assets.items())[0]
        print(f"目前 {stock_name} 價格為 {stock.price}。")
        if player.is_human:
            choice = input("是否想購買此股票？ (y/n): ").lower()
            if choice == 'y':
                player.buy_stock(stock_name, 1, stock.price)
        else:
            if player.cash > stock.price * 2:
                player.buy_stock(stock_name, 1, stock.price)

    def show_bond_options(self, player):
        print(f"{player.name} 抵達『債券市場』！")
        bond_name, bond = list(self.bonds.items())[0]
        print(f"目前 {bond_name} 價格為 {round(bond.price, 2)}。")
        if player.is_human:
            choice = input("是否想購買此債券？ (y/n): ").lower()
            if choice == 'y':
                new_bond = Bond(bond.name, bond.face_value, bond.coupon_rate, bond.maturity_turns)
                player.buy_bond(new_bond)
        else:
            if player.cash > bond.price * 1.2:
                new_bond = Bond(bond.name, bond.face_value, bond.coupon_rate, bond.maturity_turns)
                player.buy_bond(new_bond)

    def show_derivatives_options(self, player):
        print(f"{player.name} 抵達『衍生性商品交易所』！")
        print("歡迎來到衍生性商品交易所！請選擇想交易的商品：")
        print("1. 期貨 (Futures)")
        print("2. 全回報交換 (Total Return Swap, TRS)")

        if player.is_human:
            choice = input("請輸入您的選擇 (1/2, 或 n 離開)：").lower()
            if choice == '1':
                self.show_futures_options(player)
            elif choice == '2':
                self.show_trs_options(player)
            else:
                print("離開交易所。")
        else:
            strategy_choice = random.choice(['futures', 'trs', 'none'])
            if strategy_choice == 'futures':
                self.computer_futures_strategy(player)
            elif strategy_choice == 'trs':
                self.computer_trs_strategy(player)
            else:
                print(f"{player.name} 選擇不進行衍生性商品交易。")

    def show_futures_options(self, player):
        print("\n--- 期貨交易 ---")
        print("目前可交易的期貨合約：")
        for asset_name, specs in self.futures_specs.items():
            current_price = self.assets[asset_name].price
            margin_required = current_price * specs["margin_rate"]
            print(
                f"- {asset_name} 期貨: 價格 {current_price}，保證金 {round(margin_required, 2)}，到期日 {specs['maturity_turns']} 回合。")

        if player.is_human:
            choice = input("你想買入 (long)、賣出 (short) 或不交易 (n)？: ").lower()
            if choice in ["long", "short"]:
                asset_choice = input("請輸入資產名稱：")
                if asset_choice in self.assets:
                    specs = self.futures_specs[asset_choice]
                    current_price = self.assets[asset_choice].price
                    margin = current_price * specs["margin_rate"]
                    if margin > 0:
                        player.trade_futures(asset_choice, choice, current_price, margin, specs["maturity_turns"])
                else:
                    print("輸入的資產名稱無效。")

    def computer_futures_strategy(self, player):
        asset_choice = random.choice(list(self.futures_specs.keys()))
        specs = self.futures_specs[asset_choice]
        current_price = self.assets[asset_choice].price
        margin = current_price * specs["margin_rate"]

        if player.cash >= margin and random.random() > 0.5:
            direction = random.choice(["long", "short"])
            player.trade_futures(asset_choice, direction, current_price, margin, specs["maturity_turns"])
        else:
            print(f"{player.name} 選擇不進行期貨交易。")

    def show_trs_options(self, player):
        print("\n--- 全回報交換 (TRS) 交易 ---")
        print("目前可交易的 TRS 合約：")
        for asset_name, specs in self.trs_specs.items():
            current_price = self.assets[asset_name].price
            notional_value = current_price * specs["notional_value_factor"]
            margin_required = notional_value * specs["margin_rate"]
            interest_cost = notional_value * (self.central_bank.market_interest_rate + specs['interest_spread'])
            print(
                f"- {asset_name} TRS: 名義本金約 {round(notional_value, 2)}，保證金 {round(margin_required, 2)}，年化利息約 {round(interest_cost, 2)}。到期日 {specs['maturity_turns']} 回合。")

        if player.is_human:
            choice = input("你想買入 (long)、賣出 (short) 或不交易 (n)？: ").lower()
            if choice in ["long", "short"]:
                asset_choice = input("請輸入資產名稱：")
                if asset_choice in self.assets and asset_choice in self.trs_specs:
                    specs = self.trs_specs[asset_choice]
                    current_price = self.assets[asset_choice].price
                    notional_value = current_price * specs["notional_value_factor"]
                    margin = notional_value * specs["margin_rate"]
                    if player.cash >= margin:
                        player.trade_trs(
                            asset_choice,
                            choice,
                            notional_value,
                            margin,
                            specs["interest_spread"],
                            specs["maturity_turns"]
                        )
                    else:
                        print("現金不足以開立 TRS 合約。")
                else:
                    print("輸入的資產名稱無效。")

    def computer_trs_strategy(self, player):
        if player.cash < 5000 or random.random() < 0.6:
            print(f"{player.name} 選擇不進行 TRS 交易。")
            return

        asset_choice = random.choice(list(self.trs_specs.keys()))
        specs = self.trs_specs[asset_choice]
        current_price = self.assets[asset_choice].price
        notional_value = current_price * specs["notional_value_factor"]
        margin = notional_value * specs["margin_rate"]

        if player.cash >= margin:
            direction = random.choice(["long", "short"])
            player.trade_trs(
                asset_choice,
                direction,
                notional_value,
                margin,
                specs["interest_spread"],
                specs["maturity_turns"]
            )
        else:
            print(f"{player.name} 的現金不足以進行 TRS 交易。")

    def show_options_options(self, player):
        print(f"{player.name} 抵達『選擇權交易所』！")
        print("目前可交易的選擇權合約：")
        for asset_name, specs in self.options_specs.items():
            current_price = self.assets[asset_name].price
            strike_price_call = current_price * specs["strike_price_factor"]
            premium_call = self.get_option_premium('call', current_price, strike_price_call, specs["maturity_turns"])

            strike_price_put = current_price * (2 - specs["strike_price_factor"])
            premium_put = self.get_option_premium('put', current_price, strike_price_put, specs["maturity_turns"])

            print(
                f"- {asset_name} 買權: 履約價 {round(strike_price_call, 2)}, 權利金 {round(premium_call, 2)}, 到期日 {specs['maturity_turns']} 回合。")
            print(
                f"- {asset_name} 賣權: 履約價 {round(strike_price_put, 2)}, 權利金 {round(premium_put, 2)}, 到期日 {specs['maturity_turns']} 回合。")

        if player.is_human:
            choice = input("你想購買買權 (c), 賣權 (p), 或不交易 (n)？: ").lower()
            if choice in ["c", "p"]:
                asset_choice = input("請輸入資產名稱：")
                if asset_choice in self.assets and asset_choice in self.options_specs:
                    specs = self.options_specs[asset_choice]
                    current_price = self.assets[asset_choice].price

                    if choice == 'c':
                        strike_price = current_price * specs["strike_price_factor"]
                        premium = self.get_option_premium('call', current_price, strike_price, specs["maturity_turns"])
                        player.buy_option('call', asset_choice, strike_price, premium, specs["maturity_turns"])
                    else:
                        strike_price = current_price * (2 - specs["strike_price_factor"])
                        premium = self.get_option_premium('put', current_price, strike_price, specs["maturity_turns"])
                        player.buy_option('put', asset_choice, strike_price, premium, specs["maturity_turns"])
                else:
                    print("輸入的資產名稱或選擇權不支援。")
        else:
            self.computer_options_strategy(player)

    def computer_options_strategy(self, player):
        asset_choice = random.choice(list(self.options_specs.keys()))
        specs = self.options_specs[asset_choice]
        current_price = self.assets[asset_choice].price

        option_type_choice = random.choice(['call', 'put'])
        if option_type_choice == 'call':
            strike_price = current_price * specs["strike_price_factor"]
            premium = self.get_option_premium('call', current_price, strike_price, specs["maturity_turns"])
        else:
            strike_price = current_price * (2 - specs["strike_price_factor"])
            premium = self.get_option_premium('put', current_price, strike_price, specs["maturity_turns"])

        if player.cash >= premium and random.random() > 0.6:
            player.buy_option(option_type_choice, asset_choice, strike_price, premium, specs["maturity_turns"])
        else:
            print(f"{player.name} 選擇不進行選擇權交易。")

    def show_etf_options(self, player):
        print(f"{player.name} 抵達『ETF 交易所』！")
        print("歡迎來到 ETF 交易所！可供購買的 ETF 產品：")
        print("1. 科技股緩衝型ETF")
        specs = self.etf_specs["科技股緩衝型ETF"]
        print(f"   - 追蹤資產: {specs['underlying_asset']}, 價格: {specs['price']}")
        print(
            f"   - 緩衝額度: {specs['buffer'] * 100}%, 上限: {specs['cap'] * 100}%, 到期日: {specs['maturity_turns']} 回合")

        print("2. 比特幣自動贖回ETF")
        specs = self.etf_specs["比特幣自動贖回ETF"]
        current_price = self.assets[specs['underlying_asset']].price
        trigger_price = current_price * specs["trigger_price_factor"]
        print(f"   - 追蹤資產: {specs['underlying_asset']}, 價格: {specs['price']}")
        print(
            f"   - 觸發價格: {round(trigger_price, 2)}, 報酬: {specs['coupon']}, 到期日: {specs['maturity_turns']} 回合")

        if player.is_human:
            choice = input("你想購買哪種 ETF？(1/2, 或 n 離開): ").lower()
            if choice == '1':
                specs = self.etf_specs["科技股緩衝型ETF"]
                new_etf = BufferETF(
                    "緩衝型ETF", specs["underlying_asset"], specs["price"],
                    specs["maturity_turns"], specs["cap"], specs["buffer"]
                )
                new_etf.initial_underlying_price = self.assets[specs['underlying_asset']].price
                player.buy_etf(new_etf)
            elif choice == '2':
                specs = self.etf_specs["比特幣自動贖回ETF"]
                current_price = self.assets[specs['underlying_asset']].price
                trigger_price = current_price * specs["trigger_price_factor"]
                new_etf = AutocallableETF(
                    "自動贖回ETF", specs["underlying_asset"], specs["price"],
                    specs["maturity_turns"], trigger_price, specs["coupon"]
                )
                player.buy_etf(new_etf)
        else:
            self.computer_etf_strategy(player)

    def computer_etf_strategy(self, player):
        if player.cash < 5000:
            return

        choice = random.choice([1, 2])
        if choice == 1:
            specs = self.etf_specs["科技股緩衝型ETF"]
            new_etf = BufferETF(
                "緩衝型ETF", specs["underlying_asset"], specs["price"],
                specs["maturity_turns"], specs["cap"], specs["buffer"]
            )
            new_etf.initial_underlying_price = self.assets[specs['underlying_asset']].price
            player.buy_etf(new_etf)
        elif choice == 2:
            specs = self.etf_specs["比特幣自動贖回ETF"]
            current_price = self.assets[specs['underlying_asset']].price
            trigger_price = current_price * specs["trigger_price_factor"]
            new_etf = AutocallableETF(
                "自動贖回ETF", specs["underlying_asset"], specs["price"],
                specs["maturity_turns"], trigger_price, specs["coupon"]
            )
            player.buy_etf(new_etf)

    def show_cfd_options(self, player):
        print(f"{player.name} 抵達『差價合約 (CFD) 交易所』！")
        print("可用資產：", ", ".join(self.cfd_assets))

        if player.is_human:
            asset_choice = input("請輸入要交易的資產名稱：").lower()
            if asset_choice not in self.cfd_assets:
                print("輸入的資產名稱無效。")
                return

            direction_choice = input("想做多 (long) 還是做空 (short)？: ").lower()
            if direction_choice not in ["long", "short"]:
                print("輸入無效。")
                return

            try:
                margin = float(input("請輸入想投入的保證金金額："))
                leverage = int(input("請輸入槓桿倍數 (10-500)："))

                if not 10 <= leverage <= 500:
                    print("槓桿倍數必須在 10 到 500 之間。")
                    return

                if player.cash < margin:
                    print("您的現金不足以支付保證金。")
                    return

                cfd_contract = CFD(asset_choice, direction_choice, margin, leverage)
                cfd_contract.set_entry_price(self.assets[asset_choice].price)
                player.trade_cfd(asset_choice, direction_choice, margin, leverage)

            except ValueError:
                print("輸入無效。")
        else:
            self.computer_cfd_strategy(player)

    def computer_cfd_strategy(self, player):
        if player.cash < 2000 or random.random() < 0.7:
            print(f"{player.name} 選擇不進行 CFD 交易。")
            return

        asset_choice = random.choice(self.cfd_assets)
        direction_choice = random.choice(["long", "short"])
        margin = random.uniform(500, 2000)
        leverage = random.randint(10, 500)

        if player.cash >= margin:
            cfd_contract = CFD(asset_choice, direction_choice, margin, leverage)
            cfd_contract.set_entry_price(self.assets[asset_choice].price)
            player.trade_cfd(asset_choice, direction_choice, margin, leverage)
        else:
            print(f"{player.name} 的現金不足以進行 CFD 交易。")

    def show_perpetual_options(self, player):
        print(f"{player.name} 抵達『加密永續合約交易所』！")
        print("可用資產：", ", ".join(self.crypto_assets))

        if player.is_human:
            asset_choice = input("請輸入要交易的資產名稱：").lower()
            if asset_choice not in self.crypto_assets:
                print("輸入的資產名稱無效。")
                return

            direction_choice = input("想做多 (long) 還是做空 (short)？: ").lower()
            if direction_choice not in ["long", "short"]:
                print("輸入無效。")
                return

            try:
                margin = float(input("請輸入想投入的保證金金額："))
                leverage = int(input("請輸入槓桿倍數 (10-500)："))

                if not 10 <= leverage <= 500:
                    print("槓桿倍數必須在 10 到 500 之間。")
                    return

                if player.cash < margin:
                    print("您的現金不足以支付保證金。")
                    return

                contract = PerpetualContract(asset_choice, direction_choice, margin, leverage)
                contract.set_entry_price(self.assets[asset_choice].price)
                player.trade_perpetual(asset_choice, direction_choice, margin, leverage)

            except ValueError:
                print("輸入無效。")
        else:
            self.computer_perpetual_strategy(player)

    def computer_perpetual_strategy(self, player):
        if player.cash < 5000 or random.random() < 0.8:
            print(f"{player.name} 選擇不進行加密永續合約交易。")
            return

        asset_choice = random.choice(self.crypto_assets)
        direction_choice = random.choice(["long", "short"])
        margin = random.uniform(2000, 5000)
        leverage = random.randint(50, 200)

        if player.cash >= margin:
            contract = PerpetualContract(asset_choice, direction_choice, margin, leverage)
            contract.set_entry_price(self.assets[asset_choice].price)
            player.trade_perpetual(asset_choice, direction_choice, margin, leverage)
        else:
            print(f"{player.name} 的現金不足以進行加密永續合約交易。")

    def show_crypto_center_options(self, player):
        print(f"{player.name} 抵達『加密貨幣研究中心』！")
        stablecoin_price = self.assets["穩定幣"].price
        print("歡迎來到加密貨幣研究中心！您可以用穩定幣購買以下服務：")
        print(f"目前穩定幣價格為 {stablecoin_price}。")
        print("1. 避險基金合約 (500 穩定幣)")
        print("2. 專屬資訊訂閱 (100 穩定幣)")
        print("3. 市場黑天鵝保險 (200 穩定幣)")
        print("4. 加密貨幣礦機 (300 穩定幣)")
        print("5. 購買/賣出穩定幣 (USD)")

        if player.is_human:
            choice = input("請輸入您的選擇 (1-5, 或 n 離開): ").lower()

            if choice == '1':
                cost = 500 * stablecoin_price
                if player.assets['stablecoins'] * stablecoin_price >= cost and not player.assets['hedge_fund']:
                    player.assets['stablecoins'] -= 500
                    player.assets['hedge_fund'] = True
                    print(f"{player.name} 購買了避險基金合約！")
                else:
                    print("您的穩定幣不足或已擁有此合約。")
            elif choice == '2':
                cost = 100 * stablecoin_price
                if player.assets[
                    'stablecoins'] * stablecoin_price >= cost and player.name not in self.exclusive_info_turns:
                    player.assets['stablecoins'] -= 100
                    self.exclusive_info_turns[player.name] = 3
                    print(f"{player.name} 訂閱了專屬資訊，將在接下來 3 回合內獲得市場快訊！")
                else:
                    print("您的穩定幣不足或已擁有此訂閱。")
            elif choice == '3':
                cost = 200 * stablecoin_price
                if player.assets['stablecoins'] * stablecoin_price >= cost and not player.assets['insurance']:
                    player.assets['stablecoins'] -= 200
                    player.assets['insurance'] = True
                    print(f"{player.name} 購買了市場黑天鵝保險！")
                else:
                    print("您的穩定幣不足或已擁有此保險。")
            elif choice == '4':
                cost = 300 * stablecoin_price
                if player.assets['stablecoins'] * stablecoin_price >= cost and not player.assets['miner']:
                    player.assets['stablecoins'] -= 300
                    player.assets['miner'] = True
                    print(f"{player.name} 購買了加密貨幣礦機！")
                else:
                    print("您的穩定幣不足或已擁有此礦機。")
            elif choice == '5':
                action = input("您想購買 (b) 還是賣出 (s) 穩定幣？: ").lower()
                if action == 'b':
                    try:
                        amount = int(input("想購買多少穩定幣？: "))
                        cost = amount * stablecoin_price
                        if player.cash >= cost:
                            player.cash -= cost
                            player.assets['stablecoins'] += amount
                            print(f"您成功用 {round(cost, 2)} 遊戲幣購買了 {amount} 穩定幣。")
                        else:
                            print("現金不足。")
                    except ValueError:
                        print("輸入無效。")
                elif action == 's':
                    try:
                        amount = int(input("想賣出多少穩定幣？: "))
                        if player.assets['stablecoins'] >= amount:
                            revenue = amount * stablecoin_price
                            player.cash += revenue
                            player.assets['stablecoins'] -= amount
                            print(f"您成功賣出了 {amount} 穩定幣，獲得 {round(revenue, 2)} 遊戲幣。")
                        else:
                            print("穩定幣不足。")
                    except ValueError:
                        print("輸入無效。")
        else:
            self.computer_crypto_strategy(player)

    def computer_crypto_strategy(self, player):
        stablecoin_price = self.assets["穩定幣"].price
        if player.cash > 50000:
            stablecoin_to_buy = random.randint(100, 300)
            cost = stablecoin_to_buy * stablecoin_price
            if player.cash >= cost:
                player.cash -= cost
                player.assets['stablecoins'] += stablecoin_to_buy
                print(f"{player.name} 將 {round(cost, 2)} 遊戲幣換成了 {stablecoin_to_buy} 穩定幣。")

        if player.assets['stablecoins'] * stablecoin_price > 5000:
            choice = random.choice([1, 2, 3, 4])
            if choice == 1 and not player.assets['hedge_fund']:
                player.assets['stablecoins'] -= 500
                player.assets['hedge_fund'] = True
                print(f"{player.name} 購買了避險基金合約！")
            elif choice == 2 and player.name not in self.exclusive_info_turns:
                player.assets['stablecoins'] -= 100
                self.exclusive_info_turns[player.name] = 3
                print(f"{player.name} 訂閱了專屬資訊！")
            elif choice == 3 and not player.assets['insurance']:
                player.assets['stablecoins'] -= 200
                player.assets['insurance'] = True
                print(f"{player.name} 購買了市場黑天鵝保險！")
            elif choice == 4 and not player.assets['miner']:
                player.assets['stablecoins'] -= 300
                player.assets['miner'] = True
                print(f"{player.name} 購買了加密貨幣礦機！")

    def print_final_summary(self):
        print("\n--- 遊戲資產總結 ---")
        stablecoin_price = self.assets["穩定幣"].price
        for player in self.players:
            total_assets = player.cash + player.bank_account

            for stock_name, stock_info in player.assets['stocks'].items():
                current_price = self.assets[stock_name].price
                total_assets += stock_info['quantity'] * current_price

            for bond in player.assets['bonds']:
                total_assets += bond.price

            for contract in player.assets['futures']:
                underlying_asset_name = contract.underlying_asset_name
                if underlying_asset_name in self.assets:
                    current_price = self.assets[underlying_asset_name].price
                    total_assets += contract.calculate_value(current_price)

            for etf in player.assets['etfs']:
                if not isinstance(etf, AutocallableETF) or not etf.is_redeemed:
                    if etf.underlying_asset_name in self.assets:
                        current_price = self.assets[etf.underlying_asset_name].price
                        total_assets += etf.calculate_value(current_price)

            for cfd in player.assets['cfds']:
                if cfd.underlying_asset_name in self.assets:
                    current_price = self.assets[cfd.underlying_asset_name].price
                    total_assets += cfd.margin + cfd.calculate_pnl(current_price)

            for contract in player.assets['perpetual_contracts']:
                if contract.underlying_asset_name in self.assets:
                    current_price = self.assets[contract.underlying_asset_name].price
                    total_assets += contract.margin + contract.calculate_pnl(current_price)

            for contract in player.assets['trses']:
                total_assets += contract.margin

            total_assets += player.assets['stablecoins'] * stablecoin_price

            for prop in player.properties:
                total_assets += prop.price

            for lender_name, loan in player.debts.items():
                total_assets -= loan.principal

            for prop in player.mortgaged_properties:
                total_assets -= prop.mortgage_value

            status = "已破產" if player.is_bankrupt else "仍在遊戲中"
            print(f"{player.name}: 總資產 {round(total_assets, 2)} ({status})")


# --- 遊戲啟動 ---
if __name__ == "__main__":
    game = FinancialMonopolyGame()
    game.play_game(max_turns_per_round=30)