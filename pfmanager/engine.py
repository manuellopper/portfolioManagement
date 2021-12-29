from datetime import datetime
from datetime import date
from datetime import timedelta
from . import currency as cu


def imprime_portfolio(pf):
  print(" \n **************************** ") 
  print("NOMBRE DEL PORTFOLIO: ",pf.pf_name)
  print("\n* G/P Potenciales: ", pf.pot_benefit)
  print("\tG/P del producto: ", pf.pot_product_benefit)
  print("\tG/P del tipo de cambio: ", pf.pot_currency_benefit)

  print("\n* G/P Obtenidas: ", pf.current_benefit)
  print("\tG/P del producto: ", pf.current_product_benefit)
  print("\tG/P del tipo de cambio: ", pf.current_currency_benefit)

  for ass_aux in pf.assets_list:

    print(" \n ********* ACTIVO ******************* ")  
    print("Id: ",ass_aux.get_id())
    print("Nombre: ", ass_aux.asset_name)
    print("Tipo de activo: ", ass_aux.asset_type)
    print("Moneda del activo: ", ass_aux.currency)  
    print("Número acciones: ",ass_aux.get_current_shares())
    print("Valor de mercado: ", ass_aux.last_market_value)
    print("Coste subyacente: ",ass_aux.curr_cost)

    print("\n* G/P Potenciales: ", ass_aux.pot_benefit)
    print("\tG/P del producto: ", ass_aux.pot_product_benefit)
    print("\tG/P del tipo de cambio: ", ass_aux.pot_currency_benefit)

    print("\n* G/P Obtenidas: ", ass_aux.current_benefit)
    print("\tG/P del producto: ", ass_aux.current_product_benefit)
    print("\tG/P del tipo de cambio: ", ass_aux.current_currency_benefit)
  
    print("\nTotal Dividendos: ", ass_aux.total_dividends)
    print("Total Impuestos: ",ass_aux.total_taxes)
    print("Total comisiones: ", ass_aux.total_commissions )

    print("\nTotal buy shares: ", ass_aux.total_buy_shares)
    print("Total buy cost: ",ass_aux.total_buy_cost)

    print("Total sell shares: ", ass_aux.total_sell_shares)
    print("Total sell rev: ",ass_aux.total_sell_rev)

    transactions_list = ass_aux.get_transactions()

    print("Número de transacciones: ", len(transactions_list))

    for trans_aux in transactions_list:
      print(" ------- ")
      print("Id: ", trans_aux.id)
      print("Tipo: ", trans_aux.transaction_type)
      print("Fecha: ", trans_aux.date)
      if trans_aux.transaction_type=="BUY":
        print("Número: ", trans_aux.number_of_shares)
        print("Precio por acción: ", trans_aux.price_per_share)
        print("Cerradas: ", trans_aux.get_buy_closed())
      elif trans_aux.transaction_type == "SELL":
        print("Número: ", trans_aux.number_of_shares)
        print("Ingreso por acción: ", trans_aux.rev_per_share)
        print("Beneficio: ", trans_aux.operation_benefit)
      elif trans_aux.transaction_type == "DIVIDENDS":
        print("Dividendo: ", trans_aux.dividends)

      print("Comisiones: ", trans_aux.commissions)
      print("Taxes: ", trans_aux.taxes)

      print("Gross cash flow: ", trans_aux.gross_cashflow)
      print("Net cash flow: ", trans_aux.net_cashflow)

def fetch_asking_user(symbol, date_ask):
  print("Introduzca el valor unitario de ",symbol," en la fecha ",date_ask, " : ")
  return float(input())

  

# ---------------- Classes


class Portfolio:
  def __init__(self,name):
    
    ## General variables
    self.pf_name=name
    self.assets_list=[] 
    self.transactions_list=[]

    ## Total Current benefit variables
    self.current_benefit = 0
    self.current_currency_benefit = 0
    self.current_product_benefit = 0

    ## Total potential benefit variables
    self.pot_benefit = 0
    self.pot_currency_benefit = 0
    self.pot_product_benefit = 0

  def asset_exist(self, symbol=None, id=None):

    if symbol == None and id == None:
     return "Error: se debe indicar un identificador del activo (id o símbolo)"
    elif not(symbol == None) and not(id == None):
      return "Error: se debe indicar sólo uno de los parámetros symbol o id. No está permitido los dos"
    elif not(symbol == None):      
      for asset_aux in self.assets_list:
        if asset_aux.get_symbol().upper() == symbol.upper():
          return True, asset_aux   
      return False, None
    else:
      for asset_aux in self.assets_list:
        if asset_aux.get_id() == id:
          return True , asset_aux   
      return False, None

  def register_asset(self, asset_aux, copy_transactions=True):
    
    asset_type = asset_aux.get_asset_type()

    if asset_type == "Equity":
      response, r_asset = self.asset_exist(symbol=asset_aux.get_symbol())
      if response:        
        return "Error: ya existe" ## esto se puede transformar en una fusión.
      else:        
        self.assets_list.append(asset_aux)
        asset_aux.set_portfolio(self)
        if copy_transactions == True:
          self.copy_transactions_from_asset(asset_aux)
    
    self.update_portfolio(update_assets=True)
        
  def copy_transactions_from_asset(self, asset_aux):
    
    self.transactions_list.extend(asset_aux.get_transactions(copy=True))   
    self.transactions_list.sort(key=self.get_transaction_date)
    
  def register_transaction(self, transaction_aux):
    
    transaction_aux.set_portfolio(self)
    self.transactions_list.append(transaction_aux)
    if transaction_aux.get_date() < self.transactions_list[len(self.transactions_list)-1].get_date():      
      self.transactions_list.sort(key=self.get_transaction_date)  

    self.update_portfolio()

  def get_transaction_date(self, trans): return trans.get_date()

  def get_asset(self, symbol=None, id=None):
    if symbol == None and id == None:
     return "Error: se debe indicar un identificador del activo (id o símbolo)"
    elif not(symbol == None) and not(id == None):
      return "Error: se debe indicar sólo uno de los parámetros symbol o id. No está permitido los dos"
    elif not(symbol == None):
      result, asset = self.asset_exist(symbol=symbol)
      return asset
    else:
      result, asset = self.asset_exist(id=id)
      return asset
  
  def update_portfolio(self, update_assets=False):

    ## Initialize benefit variables
    self.current_benefit = 0
    self.current_currency_benefit = 0
    self.current_product_benefit = 0
    self.pot_benefit = 0
    self.pot_currency_benefit = 0
    self.pot_product_benefit = 0
    
    for asset_aux in self.assets_list:
      if update_assets == True:
        asset_aux.update_asset()
      
      self.current_benefit += asset_aux.current_benefit.get_value("LOCAL")
      self.current_currency_benefit += asset_aux.current_currency_benefit.get_value("LOCAL")
      self.current_product_benefit += asset_aux.current_product_benefit.get_value("LOCAL")
      self.pot_benefit += asset_aux.pot_benefit.get_value("LOCAL")
      self.pot_currency_benefit += asset_aux.pot_currency_benefit.get_value("LOCAL")
      self.pot_product_benefit += asset_aux.pot_product_benefit.get_value("LOCAL")

  ## aquí faltaría meter otras transacciones asociadas solo al potfolio como ingresos o retiradas, comisiones de cuenta, etc

      
    





class Asset:
  
  asset_type="Undertermined"
  
  def __init__(self, name, currency):
    
    #General variables (currency, id, name, portfolio and transactions list)
    if cu.is_currency_valid(currency):
      self.currency=currency
    else:
      return "Error" #### !!!!Hay que establecer cómo se retornan cosas

    self.set_new_id()
    self.asset_name=name    
    self.transactions_list=[]
    self.portfolio = None
    
    ## Market value variables
    self.last_market_value = cu.Currency(0,self.currency, 0, cu.get_sys_local_currency()) 
    self.last_market_value_unitary = cu.Currency(0,self.currency, 0, cu.get_sys_local_currency()) 

    ## Fetch market value variables
    self.last_market_value_fetch_date = date(1500,1,1) ## fecha muy antigua
    self.max_days_validity_mvalue = timedelta(days=1)
    self.fetch_value_method = fetch_asking_user
    
    ## Current benefit variables (total, product, currency)
    self.current_benefit=cu.Currency(0,self.currency, 0, cu.get_sys_local_currency())
    self.current_currency_benefit=cu.Currency(0,self.currency, 0, cu.get_sys_local_currency())
    self.current_product_benefit=cu.Currency(0,self.currency, 0, cu.get_sys_local_currency())
    
    # Potential benefit variables (total, product, currency)
    self.pot_benefit=cu.Currency(0,self.currency, 0, cu.get_sys_local_currency())
    self.pot_currency_benefit = cu.Currency(0,self.currency, 0, cu.get_sys_local_currency())
    self.pot_product_benefit = cu.Currency(0,self.currency, 0, cu.get_sys_local_currency())

 
       
  def set_new_id(self): self.id=datetime.timestamp(datetime.now())    
  
  def get_id(self): return self.id

  def get_asset_type(self): return self.asset_type

  def get_portfolio(self): return self.portfolio

  def set_portfolio(self, portfolio):
    if not (type(portfolio) == Portfolio):
      return "Error"
    else:
      self.portfolio=portfolio
  
  def get_transactions(self, start = 0, end = 0, id = None, copy = False):
    
    if not(id == None) and type(id) == float:
      for trans in self.transactions_list:
        if trans.get_id() == id:
          return trans

    if end == 0:
      end = len(self.transactions_list)

    if copy == True:
      return self.transactions_list[start:end].copy()
    else:
      return self.transactions_list[start:end]
   
  def get_transaction_date(self,trans): return trans.get_date()

  def fetch_value(self, value_date = None):
    if value_date == None:
      value_date = date.today()

    return self.fetch_value_method(self.symbol, value_date)
   
  
  def set_fetch_value_method(self, method, test=True):
    
    if test == True:
      temp_value = method(self.symbol, date.today())
      if not(type(temp_value) == int or type(temp_value) == float ):
        return "Error: el test no ha salido bien"

    self.fetch_value_method = method

  def set_max_days_validity_mvalue(days):
    if not (type(days)== int):
      return "Error: tipo diferente al esperado"
    self.max_days_validity_mvalue = timedelta(days=days)



   
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
    #self.last_market_value = cu.Currency(0,currency,0,cu.system_local_currency)
    self.curr_cost= cu.Currency(0,currency,0,cu.system_local_currency)    
    self.total_dividends = cu.Currency(0,currency,0,cu.system_local_currency)
    self.total_taxes= cu.Currency(0,currency,0,cu.system_local_currency)
    self.total_commissions = cu.Currency(0,currency,0,cu.system_local_currency)
    #Auxiliar variables
    self.total_buy_shares =0
    self.total_sell_shares =0 
    self.total_buy_cost = cu.Currency(0,currency,0,cu.system_local_currency)
    self.total_sell_rev = cu.Currency(0,currency,0,cu.system_local_currency)
    self.total_sell_benefit= cu.Currency(0,currency,0,cu.system_local_currency)

  def get_symbol(self): return self.symbol

  def register_transaction(self, transaction_aux, add_to_porfolio = True):
    
    type_arg= type(transaction_aux)
    if not (type_arg == TransactionBuy or type_arg == TransactionSell or type_arg== TransactionDividend or type_arg == TransactionSharesAsDividend):
      return "Error: tipo pasado no es correcto"
    
    id = transaction_aux.get_id()
    transaction_aux.set_asset(self)
    self.transactions_list.append(transaction_aux)
    self.transactions_list.sort(key=self.get_transaction_date)  
    
    if type(transaction_aux) == TransactionBuy:
      number = transaction_aux.get_number()
      self.curr_shares += number
      self.total_buy_shares += number      
      self.total_buy_cost = self.total_buy_cost + number * transaction_aux.get_price_per_share()
      self.process_buy_sell_transactions()
    elif type(transaction_aux) == TransactionSell:
      number = transaction_aux.get_number()
      self.curr_shares -= number
      self.total_sell_shares += number    
      self.total_sell_rev = self.total_sell_rev + number * transaction_aux.get_rev_per_share()
      self.process_buy_sell_transactions()
    elif type(transaction_aux) == TransactionDividend:
      self.total_dividends += transaction_aux.get_dividends()
    else:
      self.curr_shares += number
      self.total_buy_shares += number      
      self.total_buy_cost = self.total_buy_cost + number * transaction_aux.get_price_per_share()
      self.process_buy_sell_transactions()
      
    self.total_taxes = self.total_taxes + transaction_aux.get_taxes() 
    self.total_commissions = self.total_commissions + transaction_aux.get_commissions()
    
    self.update_asset()
    
    if add_to_porfolio == True and not(self.portfolio == None):
      self.portfolio.register_transaction(self.get_transactions(id=id)) 

    
  
  def get_current_shares(self): return self.curr_shares

  def process_buy_sell_transactions(self):
    buy_list = [ transaction for transaction in self.transactions_list if ( type(transaction)==TransactionBuy or type(transaction)==TransactionSharesAsDividend )]
    sell_list = [ transaction for transaction in self.transactions_list if type(transaction)==TransactionSell ]
  
    self.curr_cost = cu.Currency(0,self.currency,0,cu.system_local_currency)
    self.total_sell_benefit= cu.Currency(0,self.currency,0,cu.system_local_currency)
    
    for buy_oper in buy_list:
      buy_oper.set_buy_closed(0) #primero borro las variables buy_closed de todas las operacoines buy
      self.curr_cost = self.curr_cost + buy_oper.get_price_per_share() * buy_oper.get_number()
    
  
    for sell_oper in sell_list:
      num_sell = sell_oper.get_number()
      remaining_sell = num_sell      
      underlying_cost = cu.Currency(0,self.currency,0,cu.system_local_currency)
      for buy_oper in buy_list:        
        remaining_buy=buy_oper.get_number() - buy_oper.get_buy_closed() 
        if remaining_sell >= remaining_buy:          
          buy_oper.set_buy_closed(buy_oper.get_number())           
          underlying_cost += buy_oper.get_price_per_share() * remaining_buy
          remaining_sell -= remaining_buy
          #buy_list.remove(buy_oper)
          continue
        elif remaining_sell < remaining_buy:          
          buy_oper.set_buy_closed(buy_oper.get_buy_closed() + remaining_sell)            
          underlying_cost += buy_oper.get_price_per_share() * remaining_sell
          remaining_sell = 0
          break
        
      if remaining_sell > 0:
        return "Error: se está intentando vender más de las acciones en posesión"
      
      #update underlying cost
      sell_oper.set_underlying_cost(underlying_cost) 
      
      #update operation benefit
      operation_benefit=sell_oper.get_rev_per_share()*sell_oper.get_number()-underlying_cost
      sell_oper.operation_benefit = operation_benefit
      
      #calculate and update currency benefits for this transaction
      buy_x_rate = underlying_cost.get_value("ASSET") / underlying_cost.get_value("LOCAL")
      sell_x_rate = sell_oper.get_rev_per_share().get_value("ASSET") / sell_oper.get_rev_per_share().get_value("LOCAL")

      curr_benefit = (buy_x_rate / sell_x_rate - 1) *underlying_cost.get_value("LOCAL")
      sell_oper.currency_benefit.set_value(curr_benefit,"LOCAL")
      sell_oper.currency_benefit.set_value(0,"ASSET")

      #update product benefit (total benefit - currency benefit)
      sell_oper.product_benefit = sell_oper.operation_benefit - sell_oper.currency_benefit

      #update total benefits for selling operations
      self.total_sell_benefit= self.total_sell_benefit + operation_benefit

      #Substract this operation underlying cost from de total asset current cost
      self.curr_cost = self.curr_cost - underlying_cost

  def update_market_value(self):

    
    if (date.today() - self.max_days_validity_mvalue) > self.last_market_value_fetch_date:
      value = self.fetch_value(date.today())
      if not (type(value) == int or type(value) == float):
        return "Error: valor capturado no válido"

      self.last_market_value_fetch_date = date.today()
      resul=cu.Currency(0,self.currency,0,cu.get_sys_local_currency())
      resul.set_value(value,"ASSET")
      if not(self.currency == cu.get_sys_local_currency()):
        resul.set_value(cu.convert_currency(value,self.currency,cu.get_sys_local_currency(),self.last_market_value_fetch_date),"LOCAL")
      else:
        resul.set_value(value,"LOCAL")
        
      self.last_market_value_unitary = resul
      self.last_market_value = resul * self.curr_shares
      
      return self.last_market_value
    else:
      self.last_market_value = self.last_market_value_unitary * self.curr_shares
      return self.last_market_value
    
  def update_asset(self):

    self.update_market_value()
    
    ## Update current benefits (total, currency, product)
    self.current_benefit= self.total_sell_benefit + self.total_dividends - self.total_taxes - self.total_commissions

    self.current_currency_benefit = cu.Currency(0,self.currency,0,cu.get_sys_local_currency())
    for trans_aux in self.transactions_list:
      if trans_aux.transaction_type == "SELL":
        self.current_currency_benefit += trans_aux.currency_benefit
    
    self.current_product_benefit = self.current_benefit - self.current_currency_benefit

    # Update potential benefits (total, currency, product)

    if self.curr_shares > 0:
      self.pot_benefit= self.last_market_value - self.curr_cost

      buy_x_rate = self.curr_cost.get_value("ASSET") / self.curr_cost.get_value("LOCAL")
      potsell_x_rate = self.last_market_value.get_value("ASSET") / self.last_market_value.get_value("LOCAL")

      value = (buy_x_rate / potsell_x_rate - 1) * self.curr_cost.get_value("LOCAL")
      self.pot_currency_benefit.set_value(0,"ASSET")
      self.pot_currency_benefit.set_value(value,"LOCAL")

      self.pot_product_benefit= self.pot_benefit - self.pot_currency_benefit
   
   
    
  
class Transaction:
  
  transaction_type="Undefined"

  def __init__(self, asset_currency=cu.system_local_currency,local_currency = cu.system_local_currency, date_transaction = date.today()):
        
    self.set_new_id()
    self.asset_currency=asset_currency
    self.local_currency=local_currency
    self.portfolio_father = None
    self.asset_father = None
    self.date = date_transaction
    self.taxes = cu.Currency(0,self.asset_currency,0,self.local_currency)
    self.commissions = cu.Currency(0,self.asset_currency,0,self.local_currency)
    self.gross_cashflow = cu.Currency(0,self.asset_currency,0,self.local_currency)
    self.net_cashflow = cu.Currency(0,self.asset_currency,0,self.local_currency)
    
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
  
  transaction_type="BUY"
  
  def __init__(self, number, price_per_share, commissions=0, taxes=0, date_transaction = date.today()):
    
    if (not( type(price_per_share) == cu.Currency)) or (not(commissions == 0) and not(type(commissions) == cu.Currency)) or (not(taxes == 0) and not(type(taxes) == cu.Currency)):
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

  def get_buy_closed(self): return self.buy_closed

  def set_buy_closed(self,number_closed):
    if not(type(number_closed) == int):
      return "Error"
    
    self.buy_closed = number_closed

  
class TransactionSell(Transaction):

  transaction_type="SELL"

  def __init__(self, number, rev_per_share, commissions=0, taxes=0, date_transaction = date.today()):
    
    if (not( type(rev_per_share) == cu.Currency)) or (not(commissions == 0) and not(type(commissions) == cu.Currency)) or (not(taxes == 0) and not(type(taxes) == cu.Currency)):
      return "Error"

    super().__init__(rev_per_share.get_currency("ASSET"),rev_per_share.get_currency("LOCAL"), date_transaction)

   
    self.number_of_shares = number
    self.underlying_cost = None # El coste subyacente se establece cuando se registra la operación
    self.rev_per_share=rev_per_share
    self.operation_benefit = cu.Currency(0,self.asset_currency,0,self.local_currency)  # El beneficio se establece cuando se registra la operación
    self.currency_benefit = cu.Currency(0,self.asset_currency,0,self.local_currency)
    self.product_benefit = cu.Currency(0,self.asset_currency,0,self.local_currency)


    if not( commissions == 0 ):
      self.commissions = commissions
    
    if not( taxes == 0 ):
      self.taxes = taxes
    self.gross_cashflow = number * rev_per_share
    self.net_cashflow = self.gross_cashflow - self.commissions - self.taxes

  def get_number(self): return self.number_of_shares

  def get_rev_per_share(self): return self.rev_per_share

  def set_operation_benefit(self, benefit):
    if not(type(benefit)==cu.Currency):
      return "Error"
    
    self.operation_benefit=benefit
  
  def set_currency_benefit(self,benefit):
    if not(type(benefit)==cu.Currency):
      return "Error"
    
    self.currency_benefit=benefit

  def set_product_benefit(self,benefit):
    if not(type(benefit)==cu.Currency):
      return "Error"
    
    self.product_benefit=benefit  
  
  def get_number(self): return self.number_of_shares

  def set_underlying_cost(self, uc): 
    if not(type(uc)==cu.Currency):
      return "Error"
    
    self.underlying_cost=uc

    
class TransactionDividend(Transaction):

  transaction_type="DIVIDENDS"

  def __init__(self, dividends, commissions=0, taxes=0, date_transaction = date.today()):
    
    if (not( type(dividends) == cu.Currency)) or (not(commissions == 0) and not(type(commissions) == cu.Currency)) or (not(taxes == 0) and not(type(taxes) == cu.Currency)):
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

  transaction_type="SHARES AS DIVIDENDS"

  def __init__(self, number, price_per_share, commissions=0, taxes=0, date_transaction = date.today()):
    
    if (not( type(price_per_share) == cu.Currency)) or (not(commissions == 0) and not(type(commissions) == cu.Currency)) or (not(taxes == 0) and not(type(taxes) == cu.Currency)):
      return "Error"

    super().__init__(price_per_share.get_currency("ASSET"),price_per_share.get_currency("LOCAL"), date_transaction)
    self.number_of_shares = number
    self.price_per_share=price_per_share
    self.buy_closed=0
    self.dividends = number * price_per_share
    
    if not( commissions == 0 ):
      self.commissions = commissions
    
    if not( taxes == 0 ):
      self.taxes = taxes
    
    self.gross_cashflow = (-number) * price_per_share
    self.net_cashflow = self.gross_cashflow - self.commissions - self.taxes
  
  def get_number(self): return self.number_of_shares

  def get_price_per_share(self): return self.price_per_share

  def get_buy_closed(self): return self.buy_closed

  def set_buy_closed(self,number_closed):
    if not(number_closed == int):
      return "Error"
    
    self.buy_closed = number_closed
  
