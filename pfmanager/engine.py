from datetime import datetime
from datetime import date

# --------------- Global variables

system_local_currency = "EUR"

# --------------- Global functions

def get_sys_local_currency():
  return system_local_currency

def set_sys_local_currency(currency):
  if is_currency_valid(currency):
    system_local_currency = currency
  else:
    return "Error" #### !!!!Hay que establecer cómo se retornan cosas

def is_currency_valid(currency):
  return True

def convert_currency(value, orig_curr, dest_curr):
    #### !!!!Aquí hay que hacer la conversión
  if is_currency_valid(orig_curr) and is_currency_valid(dest_curr):
    return value
  else:
    return "Error"

# ---------------- Classes

class Currency:
  def __init__(self,asset_currency,value_asset_currency, local_currency=None, value_local_currency=None ):
    
    if is_currency_valid(asset_currency):      
      self.asset_curr=asset_currency       
    else:
      return "Error" #### !!!!Hay que establecer cómo se retornan cosas
    
    self.value_asset_curr = value_asset_currency

    if local_currency == None and value_local_currency == None:
      ## La moneda local es igual que la del activo
      self.local_curr = asset_currency
      self.value_local_curr = value_asset_currency
    elif not (local_currency == None) and value_local_currency == None:
      if is_currency_valid(local_currency):    
        self.local_curr = local_currency
        self.value_local_curr= convert_currency(value_asset_currency,asset_currency,local_currency)
      else:
        return "Error" #### !!!!Hay que establecer cómo se retornan cosas
    else:
      if is_currency_valid(local_currency):    
        self.local_curr = local_currency
        self.value_local_curr= value_local_currency
      else:
        return "Error" #### !!!!Hay que establecer cómo se retornan cosas    

  def __add__(self, other):
    return Currency(self.asset_curr,self.value_asset_curr + other.get_value("ASSET"),self.local_curr,self.value_local_curr + other.get_value("LOCAL") )
  
  def __sub__(self,other):
    return Currency(self.asset_curr,self.value_asset_curr - other.get_value("ASSET"),self.local_curr,self.value_local_curr - other.get_value("LOCAL") )

  def __mul__(self, other):
    num_type = type(other)
    if not (num_type == int or num_type == float or num_type == Currency):
      return "Error"
    elif num_type == int or num_type == float:
      return Currency(self.asset_curr,self.value_asset_curr * other,self.local_curr,self.value_local_curr * other )
    elif num_type == Currency:
      return Currency(self.asset_curr,self.value_asset_curr * other.get_value("ASSET"),self.local_curr,self.value_local_curr * other.get_value("LOCAL") )
    else:
      return "Error"

  def __rmul__(self, other):
    num_type = type(other)
    if not (num_type == int or num_type == float):
      return "Error"
    else:      
      return Currency(self.asset_curr,self.value_asset_curr * other,self.local_curr,self.value_local_curr * other )
      
  def set_value (self, value, currency ="ASSET"):    
    if currency.upper()=="ASSET":
      self.value_asset_curr = value
    elif currency.upper()=="LOCAL":
      self.value_local_curr = value
    else:
      return "Error" #### !!!!Hay que establecer cómo se retornan cosas

  def get_value (self, currency ="ASSET"):    
    if currency.upper()=="ASSET":
      return self.value_asset_curr
    elif currency.upper()=="LOCAL":
      return self.value_local_curr
    else:
      return "Error" #### !!!!Hay que establecer cómo se retornan cosas

  def get_currency (self, currency ="ASSET"):
    if currency.upper()=="ASSET":
      return self.asset_curr
    elif currency.upper()=="LOCAL":
      return self.local_curr
    else:
      return "Error" #### !!!!Hay que establecer cómo se retornan cosas



class Portfolio:
  def __init__(self,name):
    self.pf_name=name
    self.assets_list=[]
    self.transactions_list=[]

  def asset_exist(self, symbol=None):
    for i in range(len(self.assets_list)):
      if self.assets_list[i].get_symbol().upper() == symbol.upper():
        return True    
    return False

  def register_asset(self, asset_aux, copy_transactions=True):
    
    asset_type = asset_aux.get_asset_type()
    
    if asset_type == "Equity":
      if self.asset_exist(symbol=asset_aux.get_symbol()):
        return "Error: ya existe" ## esto se puede transformar en una fusión.
      else:
        self.assets_list.append(asset_aux)
        asset_aux.set_portfolio(self)
        if copy_transactions == True:
          self.copy_transactions_from_asset(self,asset_aux)
        
  def copy_transactions_from_asset(self, asset_aux):
    self.transactions_list.append(asset_aux.get_transactions(copy=True))
    ## !! Aquí habría que ordena la lista de transacciones.. por fecha, por ejemplo
  
  def add_transaction(self, transaction_aux):
    
    transaction_aux.set_portfolio(self)

    if transaction_aux.get_date() >= self.transactions_list[len(self.transactions_list)-1].get_date():
      self.transactions_list.append(transaction_aux)
    else:
      self.transaction_list.sort(key=self.get_transaction_date)  

  def get_transaction_date(self, trans): return trans.get_date()


class Asset:
  
  asset_type="Undertermined"
  
  def __init__(self, name, currency):
    self.set_new_id()
    self.asset_name=name    
    self.transactions_list=[]
    self.portfolio = None
    if is_currency_valid(currency):
      self.currency=currency
    else:
      return "Error" #### !!!!Hay que establecer cómo se retornan cosas
       
  def set_new_id(self): self.id=datetime.timestamp(datetime.now())    
  
  def get_id(self): return self.id

  def get_asset_type(self): return self.asset_type

  def get_portfolio(self): return self.portfolio

  def set_portfolio(self, portfolio):
    if not (type(portfolio) == Portfolio):
      return "Error"
    else:
      self.portfolio=portfolio
  
  def get_transactions(self, start = 0, end = len(self.transactions_list), copy = False):
    
    if copy == True:
      return self.transactions_list[start:end].copy()
    else:
      return self.transactions_list[start:end]
  
  def add_transaction(self, transaction_aux, add_to_porfolio = True):
    
    transaction_aux.set_asset(self)
    if transaction_aux.get_date() >= self.transactions_list[len(self.transactions_list)-1].get_date():
      self.transactions_list.append(transaction_aux)
    else:
      self.transaction_list.sort(key=self.get_transaction_date)  
    
    if add_to_porfolio == True and not(self.portfolio == None):
      self.portfolio.add_transaction(transaction_aux)
    
  def get_transaction_date(self,trans): return trans.get_date()

   
class AssetEquity(Asset):

  def __init__(self, name, currency, symbol, sector=None,market_type=None, size=None, caract=None):
    # Main information
    super().__init__(name,currency)  
    self.asset_type="Equity"
    self.symbol = symbol
    #Asset general information
    self.sector=sector
    self.market_type=market_type
    self.size=size
    self.caract=caract
    #Asset internal KPI
    self.curr_shares = 0
    self.market_value = Currency(currency,0,system_local_currency,0)
    self.curr_cost= Currency(currency,0,system_local_currency,0)    
    self.total_dividends = Currency(currency,0,system_local_currency,0)
    self.total_taxes= Currency(currency,0,system_local_currency,0)
    self.total_commissions = Currency(currency,0,system_local_currency,0)
    #Auxiliar variables
    self.total_buy_shares =0
    self.total_sell_shares =0 
    self.total_buy_cost = Currency(currency,0,system_local_currency,0)
    self.total_sell_rev = Currency(currency,0,system_local_currency,0)

  def get_symbol(self): return self.symbol

  def register_buy(self,transaction_aux):
    
    number= transaction_aux.get_number()
    price_per_share= transaction_aux.get_price_per_share()
    commissions= transaction_aux.get_commissions()
    taxes=transaction_aux.get_taxes()

    self.add_transaction(transaction_aux)

    self.curr_shares += number
    self.total_buy_shares += number
    self.curr_cost = self.curr_cost + number * price_per_share
    self.total_buy_cost = self.total_buy_cost + number * price_per_share

    self.total_taxes = self.taxes + taxes  
    self.total_commissions = self.total_commisions + commissions

  def register_sell(self, transaction_aux):
    
    number= transaction_aux.get_number()
    rev_per_share= transaction_aux.get_rev_per_share()
    commissions= transaction_aux.get_commissions()
    taxes=transaction_aux.get_taxes()

    if self.curr_shares < number:
      return "Error: no se puede compar más de lo que hay"
    
    u_cost = self.underlying_cost(number)
    transaction_aux.set_operation_benefit(number * rev_per_share - u_cost)    
    self.update_buy_closed(number) # de las transsacciones buy actualizar las buy_closed
    self.add_transaction(transaction_aux)

    self.curr_shares -= number
    self.total_sell_shares += number
    # self.curr_cost = self.curr_cost + number * price_per_share
    self.total_sell_rev = self.total_sell_rev + number * price_per_share

    self.total_taxes = self.taxes + taxes  
    self.total_commissions = self.total_commisions + commissions


  def register_dividend(self,transaction_aux):
    
    commissions= transaction_aux.get_commissions()
    taxes=transaction_aux.get_taxes()
    dividends=transaction_aux.get_dividends()
  
    self.add_transaction(transaction_aux)

    self.total_taxes = self.taxes + taxes    
    self.total_commissions = self.total_commisions + commissions

  def register_shares_as_dividend(self,transaction_aux):
    
    number= transaction_aux.get_number()
    price_per_share= transaction_aux.get_price_per_share()
    commissions= transaction_aux.get_commissions()
    taxes=transaction_aux.get_taxes()

    self.add_transaction(transaction_aux)

    self.curr_shares += number
    self.total_buy_shares += number
    self.curr_cost = self.curr_cost + number * price_per_share
    self.total_buy_cost = self.total_buy_cost + number * price_per_share

    self.total_taxes = self.taxes + taxes  
    self.total_commissions = self.total_commisions + commissions

  def register_transaction(self, transaction_aux):
    
    if type(transaction_aux == TransactionBuy):
      self.register_buy(transaction_aux)    
    elif type(transaction_aux == TransactionSell):
      self.register_sell(transaction_aux)
    elif type(transaction_aux == TransactionDividend):
      self.register_dividend(transaction_aux)
    elif type(transaction_aux == TransactionSharesAsDividend):
      self.register_shares_as_dividend(transaction_aux)
    else:
      return "Error"
  
  def get_current_shares(self): return self.curr_shares

  def underlying_cost(self,number):  pass

  def update_buy_closed(self, number): pass

  
class Transaction:
  
  def __init__(self, asset_currency=system_local_currency,local_currency = system_local_currency, date_transaction = date.today()):
        
    self.set_new_id()
    self.asset_currency=asset_currency
    self.local_currency=local_currency
    self.portfolio_father = None
    self.asset_father = None
    self.date = date_transaction
    self.taxes = Currency(self.asset_currency,0,self.local_currency,0)
    self.commissions = Currency(self.asset_currency,0,self.local_currency,0)
    self.gross_cashflow = Currency(self.asset_currency,0,self.local_currency,0)
    self.net_cashflow = Currency(self.asset_currency,0,self.local_currency,0)    
    
  def set_new_id(self): self.id=datetime.timestamp(datetime.now())

  def get_id(self): return self.id

  def set_asset(self, asset_aux):
    ## comprobar si es algún tipo de asset.. es decir si el typo es hijo de Asset
    self.asset_father=asset_aux

  def get_commissions(self): return self.commissions

  def get_taxes(self): return self.taxes

  def get_date(self): return self.date

  def set_portfolio(self, pf): self.portfolio_father = pf 

   
class TransactionBuy(Transaction):
  def __init__(self, number, price_per_share, commissions=0, taxes=0, date_transaction = date.today()):
    
    if (not( type(price_per_share) == Currency)) or (not(commissions == 0) and not(type(commissions) == Currency)) or (not(taxes == 0) and not(type(taxes) == Currency)):
      return "Error"

    super().__init__(price_per_share.get_currency("ASSET"),price_per_share.get_currency("LOCAL"), date_transaction)
    self.number_of_shares = number
    self.price_per_share=price_per_share
    self.buy_closed=0

    if not( commissions == 0 ):
      self.commissions = commissions
    
    if not( taxes == 0 ):
      self.taxes = taxes
    
    self.gross_cashflow = (-number) * price_per_share
    self.net_cashflow = self.gross_cashflow - self.commissions - self.taxes
  
  def get_number(self): return self.number_of_shares

  def get_price_per_share(self): return self.price_per_share

  
class TransactionSell(Transaction):
  def __init__(self, number, rev_per_share, commissions=0, taxes=0, date_transaction = date.today()):
    
    if (not( type(rev_per_share) == Currency)) or (not(commissions == 0) and not(type(commissions) == Currency)) or (not(taxes == 0) and not(type(taxes) == Currency)):
      return "Error"

    super().__init__(rev_per_share.get_currency("ASSET"),rev_per_share.get_currency("LOCAL"), date_transaction)

   
    self.number_of_shares = number
    self.rev_per_share=rev_per_share
    self.operation_benefit = None  # El beneficio se establece cuando se registra la operación
    
    if not( commissions == 0 ):
      self.commissions = commissions
    
    if not( taxes == 0 ):
      self.taxes = taxes
    self.gross_cashflow = number * price_per_share
    self.net_cashflow = self.gross_cashflow - self.commissions - self.taxes

  def get_number(self): return self.number_of_shares

  def get_rev_per_share(self): return self.rev_per_share

  def set_operation_benefit(self, benefit):
    if not(type(benefit)==Currency):
      return "Error"
    
    self.operation_benefit=benefit
    
class TransactionDividend(Transaction):
  def __init__(self, dividends, commissions=0, taxes=0, date_transaction = date.today()):
    
    if (not( type(dividends) == Currency)) or (not(commissions == 0) and not(type(commissions) == Currency)) or (not(taxes == 0) and not(type(taxes) == Currency)):
      return "Error"

    super().__init__(dividends.get_currency("ASSET"),dividends.get_currency("LOCAL"),date_transaction)

    self.dividends=dividends
    
    if not( commissions == 0 ):
      self.commissions = commissions
    
    if not( taxes == 0 ):
      self.taxes = taxes
    
    self.gross_cashflow = dividends
    self.net_cashflow = self.gross_cashflow - self.commissions - self.taxes

  def get_dividends(self): return self.dividends
    
      
class TransactionSharesAsDividend(Transaction):
  def __init__(self, number, price_per_share, commissions=0, taxes=0, date_transaction = date.today()):
    
    if (not( type(price_per_share) == Currency)) or (not(commissions == 0) and not(type(commissions) == Currency)) or (not(taxes == 0) and not(type(taxes) == Currency)):
      return "Error"

    super().__init__(price_per_share.get_currency("ASSET"),price_per_share.get_currency("LOCAL"), date_transaction)
    self.number_of_shares = number
    self.price_per_share=price_per_share
    self.buy_closed=0
    
    if not( commissions == 0 ):
      self.commissions = commissions
    
    if not( taxes == 0 ):
      self.taxes = taxes
    
    self.gross_cashflow = (-number) * price_per_share
    self.net_cashflow = self.gross_cashflow - self.commissions - self.taxes
  
  def get_number(self): return self.number_of_shares

  def get_price_per_share(self): return self.price_per_share
  
