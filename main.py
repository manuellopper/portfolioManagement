import pfmanager.engine as pm
import datetime as datetime

pf=pm.Portfolio("De Giro")
asset1 = pm.AssetEquity("Telefónica SA","EUR","TEF")
asset2 = pm.AssetEquity("Medical Properties","USD","MPW")
asset3 = pm.AssetEquity("Apple","USD","AAPL")

tr1 = pm.TransactionBuy(10,pm.Currency("USD",100,"EUR",80),pm.Currency("USD",2,"EUR",1.5),date_transaction=datetime.datetime(2021,5,3) )

print(asset3.register_transaction(tr1))

