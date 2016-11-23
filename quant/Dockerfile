FROM python:2.7

RUN apt-get update
RUN apt-get install python-pip --yes
RUN pip install Quandl 
RUN pip install pandas
RUN pip install requests
RUN pip install matplotlib
COPY main.py /root/
COPY mcap_token.py /root/
RUN chmod +x /root/main.py
ENTRYPOINT [ "/root/main.py" ]

