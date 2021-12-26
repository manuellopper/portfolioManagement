import pfmanager.engine as pm
from datetime import date

pf=pm.Portfolio("De Giro")
pf.register_asset(pm.AssetEquity("Telefónica SA","EUR","TEF"))


tr1 = pm.TransactionBuy(10,pm.Currency("EUR",100),pm.Currency("EUR",2.5),date_transaction=date(2020,5,3) )

pf.get_asset(symbol="TEF").register_transaction(tr1)

tr2 = pm.TransactionBuy(5,pm.Currency("EUR",110),pm.Currency("EUR",2.5),date_transaction=date(2020,6,4) )

pf.get_asset(symbol="TEF").register_transaction(tr2)

tr3 = pm.TransactionSell(4,pm.Currency("EUR",115),pm.Currency("EUR",2.5),date_transaction=date(2021,2,10) )

pf.get_asset(symbol="TEF").register_transaction(tr3)

tr4 = pm.TransactionSell(10,pm.Currency("EUR",110),pm.Currency("EUR",2.5),date_transaction=date(2021,5,12) )

pf.get_asset(symbol="TEF").register_transaction(tr4)



for ass_aux in pf.assets_list:
  
  print(" ************************************* ")
  
  print(ass_aux.get_id(), ass_aux.asset_name, ass_aux.currency, ass_aux.asset_type)
  

  
  print("Número acciones: ",ass_aux.get_current_shares(), "Coste subyacente: ",ass_aux.curr_cost)
  
  print("Dividendos: ", ass_aux.total_dividends, "Taxes: ",ass_aux.total_taxes, "Commissions: ", ass_aux.total_commissions )

  print("Total buy shares: ", ass_aux.total_buy_shares, "Total buy cost: ",ass_aux.total_buy_cost)

  print("Total sell shares: ", ass_aux.total_sell_shares, "Total sell rev: ",ass_aux.total_sell_rev)

  transactions_list = ass_aux.get_transactions()

  print("Número de transacciones: ", len(transactions_list))

  for trans_aux in transactions_list:
    print(" ------- ")
    print("Id: ", trans_aux.id)
    print("Tipo: ", trans_aux.transaction_type, "Fecha: ", trans_aux.date)
    if trans_aux.transaction_type=="BUY":
      print("Número: ", trans_aux.number_of_shares , "Precio por acción: ", trans_aux.price_per_share, "Cerradas: ", trans_aux.get_buy_closed())
    elif trans_aux.transaction_type == "SELL":
      print("Número: ", trans_aux.number_of_shares , "Ingreso por acción: ", trans_aux.rev_per_share, "Beneficio: ", trans_aux.operation_benefit)

    print("Comisiones: ", trans_aux.commissions, "Taxes: ", trans_aux.taxes)

    print("Gross cash flow: ", trans_aux.gross_cashflow, "Net cash flow: ", trans_aux.net_cashflow)