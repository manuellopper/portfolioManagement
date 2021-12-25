import pfmanager.engine as pm
from datetime import date

pf=pm.Portfolio("De Giro")
asset1 = pm.AssetEquity("Telefónica SA","EUR","TEF")
asset2 = pm.AssetEquity("Medical Properties","USD","MPW")
asset3 = pm.AssetEquity("Apple","USD","AAPL")
pf.register_asset(asset1)
pf.register_asset(asset2)
pf.register_asset(asset3)
print(len(pf.assets_list))

### COMPRO 10 ACCIONES DE APPLE POR 10 USD CADA UNA

tr1 = pm.TransactionBuy(10,pm.Currency("USD",100,"EUR",80),pm.Currency("USD",2,"EUR",1.5),date_transaction=date(2021,5,3) )

print(asset3.register_transaction(tr1))

### COMPRO 20 ACCIONES DE TELEFÓNICA POR 50 EUR CADA UNA

tr2 = pm.TransactionBuy(20,pm.Currency("EUR",50),pm.Currency("EUR",2,5),date_transaction=date(2020,8,4) )

print(asset1.register_transaction(tr2))

### COMPRO 9 ACCIONES DE MEDICAL PROPERTIES POR 9 USD CADA UNA

tr3 = pm.TransactionBuy(9,pm.Currency("USD",150,"EUR",120),pm.Currency("USD",1,"EUR",0.7),date_transaction=date(2021,7,7) )

print(asset2.register_transaction(tr3))
#print(pf.get_asset(symbol="MPW").register_transaction(tr3))

## VENDO 5 ACCINES DE MEDICAL PROPERTIES POR 140  USD CADA UNA

tr4 = pm.TransactionSell(5,pm.Currency("USD",140,"EUR",130),pm.Currency("USD",2,"EUR",1.5),date_transaction=date(2021,12,1) )

##print(pf.get_asset(symbol="MPW").register_transaction(tr4))
print(asset2.register_transaction(tr4))

## VENDO 20 ACCINES DE TELEFÓNICA POR 55 EUR CADA UNA

tr5 = pm.TransactionSell(20,pm.Currency("EUR",55),pm.Currency("EUR",1.5),date_transaction=date(2021,12,2) )

#print(pf.get_asset(symbol="TEF").register_transaction(tr5))
print(asset1.register_transaction(tr5))
## Imprimo todo

print(len(pf.assets_list))

for ass_aux in pf.assets_list:
  print(ass_aux.get_id(), ass_aux.asset_name, ass_aux.currency, ass_aux.asset_type)
  

  print(" ************************************* ")
  print("Número acciones: ",ass_aux.get_number(), "Coste subyacente: ",ass_aux.curr_cost)
  
  print("Dividendos: ", ass_aux.total_dividends, "Taxes: ",ass_aux.total_taxes, "Commissions: ", ass_aux.total_commissions )

  print("Total buy shares: ", ass_aux.total_buy_shares, "Total buy cost: ",ass_aux.total_buy_cost)

  print("Total sell shares: ", ass_aux.total_sell_shares, "Total buy cost: ",ass_aux.total_sell_rev)

  transactions_list = ass_aux.get_transactions()

  print("Número de transacciones: ", len(transactions_list))

  for trans_aux in transactions_list:
    print(" ------- ")
    print("Id: ", trans_aux.id)
    print("Tipo: ", trans_aux.transaction_type, "Fecha: ", trans_aux.date)
    if trans_aux.transaction_type=="BUY":
      print("Número: ", trans_aux.number_of_shares , "Precio por acción: ", trans_aux.price_per_share, "Cerradas: ", trans_aux.buy_closed)
    elif trans_aux.transaction_type == "SELL":
      print("Número: ", trans_aux.number_of_shares , "Ingreso por acción: ", trans_aux.rev_per_share, "Beneficio: ", trans_aux.operation_benefit)
    
    print("Comisiones: ", trans_aux.total_commissions, "Taxes: ", trans_aux.total_taxes)

    print("Gross cash flow: ", trans_aux.gross_cash_flow, "Net cash flow: ", trans_aux.net_cash_flow)



