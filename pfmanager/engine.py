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

  print(" ********** CUENTA ASOCIADA A PORTFOLIO *********")
  print("Nombre: ", pf.account.name)
  keys = pf.account.balance.keys()
  for key in keys:
    print("Balance en ",key,": ",pf.account.balance[key]," ",key)
  
  for record_aux in pf.account.list_of_records:
    print("--------------")
    print("Id: ",record_aux.id, " - Tipo: ",record_aux.record_type)
    print("Fecha: ",record_aux.record_time)
    print("Moneda: ",record_aux.currency)
    print("Saldo anterior: ", record_aux.prev_balance," ", record_aux.currency)
    print("Flujo de caja: ", record_aux.cash_flow , " ", record_aux.currency)
    print("Saldo Posterior: ", record_aux.result_balance," ", record_aux.currency)





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
    self.account = None

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

  def register_asset(self, asset_aux, register_records=True):
    
    asset_type = asset_aux.get_asset_type()

    if asset_type == "Equity":
      response, r_asset = self.asset_exist(symbol=asset_aux.get_symbol())
      if response:        
        return "Error: ya existe" ## esto se puede transformar en una fusión.
      else:        
        self.assets_list.append(asset_aux)
        asset_aux.set_portfolio(self)
        if register_records == True and self.account is not None:
          for trans_aux in asset_aux.transactions_list:
            trans_aux.generate_records(self.account)
    
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
    if cu.Currency.is_currency_valid(currency):
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

  def register_transaction(self, transaction_aux, register_records = True):
    
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
    
    if (register_records == True) and (self.portfolio is not None):
      if self.portfolio.account is not None:
        transaction_aux.generate_records(self.portfolio.account)
         

    
  
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
        resul.set_value(cu.Currency.convert_currency(value,self.currency,cu.get_sys_local_currency(),self.last_market_value_fetch_date),"LOCAL")
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

  def generate_records(self, acc_aux): pass


   
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

  def generate_records(self, acc_aux):

    records_list = []
    gross_cash_flow= self.number_of_shares* self.price_per_share
    if not( gross_cash_flow.get_currency("ASSET") == gross_cash_flow.get_currency("LOCAL") ):
      #hay que registrar cambio de divisa
      #primero hay que quitar de la divisa local
      records_list.append(Record(-gross_cash_flow.get_value("LOCAL"),curr=gross_cash_flow.get_currency("LOCAL"),assoc_trans=self, rec_time=self.date,rec_type="Money exchange"))
      #sumamos a la divisa del activo 
      records_list.append(Record(gross_cash_flow.get_value("ASSET"),curr=gross_cash_flow.get_currency("ASSET"),assoc_trans=self, rec_time=self.date,rec_type="Money exchange"))

    #se deduce de la moneda del activo el importe bruto a comprar
    records_list.append(Record(-gross_cash_flow.get_value("ASSET"),curr=gross_cash_flow.get_currency("ASSET"),assoc_trans=self, rec_time=self.date,rec_type="Buy"))

    if not( self.commissions == 0):
      #restamos las comisiones en la moneda local
      records_list.append(Record(-self.commissions.get_value("LOCAL"),curr=self.commissions.get_currency("LOCAL"),assoc_trans=self, rec_time=self.date,rec_type="Commissions"))

    
    acc_aux.register_record(records_list)

  
  
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
  
  def generate_records(self, acc_aux):
    
    records_list = []
    gross_cash_flow= self.number_of_shares* self.rev_per_share

    #se incrementa de la moneda del activo el importe de la venta
    records_list.append(Record(gross_cash_flow.get_value("ASSET"),curr=gross_cash_flow.get_currency("ASSET"),assoc_trans=self, rec_time=self.date,rec_type="Sell"))

    if not( gross_cash_flow.get_currency("ASSET") == gross_cash_flow.get_currency("LOCAL") ):
      #hay que registrar cambio de divisa
      #primero hay que quitar de la moneda del activo
      records_list.append(Record(-gross_cash_flow.get_value("ASSET"),curr=gross_cash_flow.get_currency("ASSET"),assoc_trans=self, rec_time=self.date,rec_type="Money exchange"))
      #sumamos a la divisa local
      records_list.append(Record(gross_cash_flow.get_value("LOCAL"),curr=gross_cash_flow.get_currency("LOCAL"),assoc_trans=self, rec_time=self.date,rec_type="Money exchange"))

    if not( self.commissions == 0):
      #restamos las comisiones de la moneda local
      records_list.append(Record(-self.commissions.get_value("LOCAL"),curr=self.commissions.get_currency("LOCAL"),assoc_trans=self, rec_time=self.date,rec_type="Commissions"))

    acc_aux.register_record(records_list)

    
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

  def generate_records(self, acc_aux):
    records_list = []
    gross_cash_flow= self.dividends

    #se incrementa de la moneda del activo el importe del dividendo
    records_list.append(Record(gross_cash_flow.get_value("ASSET"),curr=gross_cash_flow.get_currency("ASSET"),assoc_trans=self, rec_time=self.date,rec_type="Dividend"))

    ## se decrementa en la moneda del activo el importe de la retención
    if not( self.taxes == 0):
      #restamos la retención de la moneda del activo
      records_list.append(Record(-self.taxes.get_value("ASSET"),curr=self.taxes.get_currency("ASSET"),assoc_trans=self, rec_time=self.date,rec_type="Taxes"))
      
      net_cash_flow= gross_cash_flow - self.taxes
    else:
      net_cash_flow= gross_cash_flow
    

    if not( net_cash_flow.get_currency("ASSET") == net_cash_flow.get_currency("LOCAL") ):
      #hay que registrar cambio de divisa
      #primero hay que quitar de la moneda del activo
      records_list.append(Record(-net_cash_flow.get_value("ASSET"),curr=net_cash_flow.get_currency("ASSET"),assoc_trans=self, rec_time=self.date,rec_type="Money exchange"))
      #sumamos a la divisa local
      records_list.append(Record(net_cash_flow.get_value("LOCAL"),curr=net_cash_flow.get_currency("LOCAL"),assoc_trans=self, rec_time=self.date,rec_type="Money exchange"))
      

    if not( self.commissions == 0):
      #restamos las comisiones de la moneda local
      records_list.append(Record(-self.commissions.get_value("LOCAL"),curr=self.commissions.get_currency("LOCAL"),assoc_trans=self, rec_time=self.date,rec_type="Commissions"))

    acc_aux.register_record(records_list)
    
      
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
  
  def generate_records(self, acc_aux):
    pass
  

class Account:
  def __init__ (self, name):
    
    self.name= name
    self.list_of_portfolios = []
    self.list_of_records = []
    self.balance = {cu.system_local_currency: 0} # Se inicia sólo con la currency local del sistema

  def register_portfolio(self , pf , generate_records = True):
    if type(pf) is not Portfolio:
      return "Error: tipo no válido"

    if pf in self.list_of_portfolios:
      return "Ya se encuentra registrado"
    
    self.list_of_portfolios.append(pf)
    pf.account=self

    if generate_records == True:
      for asset_aux in pf.assets_list:
        for trans_aux in asset_aux.transactions_list:
          trans_aux.generate_records(self) 

  
  def register_record(self, rec):
    
    ## rec puede ser un objeto de tipo Record o bien una lista de objetos de tipo Record

    if type(rec) == list:
      if type(rec[0]) is not Record:
        return "Error:tipos no válidos"      
      self.list_of_records.extend(rec)
    elif type(rec) == Record:
      self.list_of_records.append(rec)
    else:
      return "Error: tipo no válido"

    
    self.list_of_records.sort(key=self.get_record_date)

    ## para los registros que tengan igual date se ordena por id de los mismos (el id es un timestamp)
    start_index=None
    end_index=None
    list_aux=[]
    for i in range(0,len(self.list_of_records)):        
      if i == 0:
        continue
      if self.list_of_records[i].record_time == self.list_of_records[i-1].record_time:
        if start_index == None:
          start_index=i-1          
        end_index=i+1
      else:
        if not( start_index == None ):
          list_aux = self.list_of_records[start_index:end_index].copy()
          list_aux.sort(key=self.get_record_id)
          self.list_of_records[start_index:end_index]=list_aux
          start_index = None
          end_index= None
      
      if i == (len(self.list_of_records)-1) and not (start_index==None):
        list_aux = self.list_of_records[start_index:end_index].copy()        
        list_aux.sort(key=self.get_record_id)
        self.list_of_records[start_index:end_index]=list_aux
        start_index = None
        end_index= None

    # se actualiza el balance
    keys= self.balance.keys()
    for key in keys:
      self.balance[key]=0
    
    for rec_aux in self.list_of_records:
      curr=rec_aux.currency

      if curr not in keys:
        self.balance[curr]=0
        keys=self.balance.keys()

      rec_aux.prev_balance = self.balance[curr]
      self.balance[curr]+=rec_aux.cash_flow
      rec_aux.result_balance = self.balance[curr]


  def get_record_date(self, rec): return rec.record_time

  def get_record_id(self, rec): return rec.id







class Record:
  def __init__(self,cash_flow, rec_type="Undetermined", curr = cu.system_local_currency , desc = "", assoc_trans = None, rec_time = datetime.now() ):
    
    self.set_new_id()
    self.record_type = rec_type
    self.record_time = rec_time
    self.currency = curr
    self.prev_balance = 0
    self.result_balance = 0
    self.cash_flow = cash_flow
    self.description = desc
    self.associated_transaction = assoc_trans

  def set_new_id(self): 
    self.id=datetime.timestamp(datetime.now())
    




