import pfmanager.engine as pm
import pfmanager.currency as cu
from datetime import date

pf=pm.Portfolio("De Giro")
asset1 = pm.AssetEquity("Telefónica SA","EUR","TEF")
asset2 = pm.AssetEquity("Medical Properties","USD","MPW")
asset3 = pm.AssetEquity("Apple","USD","AAPL")
pf.register_asset(asset1)
pf.register_asset(asset2)
pf.register_asset(asset3)


### COMPRO 10 ACCIONES DE APPLE POR 10 USD CADA UNA

tr1 = pm.TransactionBuy(10,cu.Currency("USD",100,"EUR",80),cu.Currency("USD",2,"EUR",1.5),date_transaction=date(2021,5,3) )


pf.get_asset(symbol="AAPL").register_transaction(tr1)

### COMPRO 20 ACCIONES DE TELEFÓNICA POR 50 EUR CADA UNA

tr2 = pm.TransactionBuy(20,cu.Currency("EUR",50),cu.Currency("EUR",2.5),date_transaction=date(2020,8,4) )


pf.get_asset(symbol="TEF").register_transaction(tr2)

### COMPRO 9 ACCIONES DE MEDICAL PROPERTIES POR 9 USD CADA UNA

tr3 = pm.TransactionBuy(9,cu.Currency("USD",150,"EUR",120),cu.Currency("USD",1,"EUR",0.7),date_transaction=date(2021,7,7) )


pf.get_asset(symbol="MPW").register_transaction(tr3)

## VENDO 5 ACCINES DE MEDICAL PROPERTIES POR 140  USD CADA UNA

tr4 = pm.TransactionSell(5,cu.Currency("USD",140,"EUR",130),cu.Currency("USD",2,"EUR",1.5),date_transaction=date(2021,12,1) )

pf.get_asset(symbol="MPW").register_transaction(tr4)


## VENDO 10 ACCINES DE Apple POR 55 EUR CADA UNA

tr5 = pm.TransactionSell(10,cu.Currency("USD",110,"EUR",100),cu.Currency("USD", 2,"EUR",1.5),date_transaction=date(2021,12,2) )

pf.get_asset(symbol="AAPL").register_transaction(tr5)

## Imprimo todo
pm.imprime_portfolio(pf)
