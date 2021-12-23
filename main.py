import pfmanager.engine as pm


pf=pm.Portfolio("Portfolio de Prueba")
as1=pm.Asset("Telefónica SA","EUR")
as2=pm.AssetEquity("Iberdrola","EUR","IBR",pf,add_to_porfolio = True)
d=pm.Transaction()
e=pm.TransactionBuyEquity()
f=pm.TransactionSellEquity()
g=pm.TransactionDividendEquity()
h=pm.TransactionDividendWithSharesEquity()
curr1=pm.Currency("EUR",12)
curr2=pm.Currency("EUR",14,"USD")


print(pf.pf_name)
print("Assets en el porfolio:")
for i in range(len(pf.assets_list)):  
  print(pf.assets_list[i].get_symbol())

print(f"Asset - Id: {as1.get_id()} Asset Type: {as1.asset_type} Nombre: {as1.asset_name} Currency: {as1.currency} Portfolio: {as1.portfolio.pf_name}")
print(f"Asset - Id: {as2.get_id()} Asset Type: {as2.asset_type} Nombre: {as2.asset_name} Symbol: {as2.symbol} Currency: {as2.currency} Portfolio: {as2.portfolio.pf_name}")
print(f"Currency {curr1.asset_curr} Value {curr1.value_asset_curr} // Currency {curr1.local_curr} Value {curr1.value_local_curr}")
print(f"Currency {curr2.asset_curr} Value {curr2.value_asset_curr} // Currency {curr2.local_curr} Value {curr2.value_local_curr}")

print(d.get_id())
print(e.get_id())
print(f.get_id())
print(g.get_id())
print(h.get_id())

