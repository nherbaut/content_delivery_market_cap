This contains the sources for a graph-generator displaying the market capitalization of the stakeholders of the content delivery market.

first you need to have a quantl API token, you can get it for free (as in free beer) from here: https://blog.quandl.com/getting-started-with-the-quandl-api
then copy the file quant/mcap_token.py.tpl to quant/mcap_token.py and replace the token

to build the software, just type the following command:
```
% cd quant
% docker build . -- nherbaut/mcap
```

then to run the software, type

```
% docker run nherbaut/mcap --start_year 2013 --stdout > res.png
```

the result file will contains the graphs.

