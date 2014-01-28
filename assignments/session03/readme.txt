Instruction to execute the code

The current code searches for "macbook pro 13 retina " from Ebay and Amazon and give their prices
First the prices, product and a URL from ebay search is displayed
Next, amazon search for the same product, its price and product are displayed
finally, amazon lookup returns the reviews of the product
currently the code is hard coded for searching with 'macbook pro 13 retina'.
but it is trivial to change to search for other products

Amazon api requests is not simple as I thought. It is too complicated than ebay.
I used a python wrapper for Amazon product search.
It is available here;http://python-amazon-product-api.readthedocs.org/en/latest/index.html#
download to virtualenv is required
pip install python-amazon-product-api

Next you require lxml module, since both ebay and amazon api does not return JSON object
for parsing.
for mac install using the following:
STATIC_DEPS=true sudo pip install lxml

Now you everything is installed

python amazon_ebay_search.py would print results to the console
