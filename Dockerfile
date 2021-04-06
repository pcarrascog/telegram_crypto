FROM python:alpine
RUN pip install requests python-telegram-bot --upgrade 
RUN mkdir /app
ADD bot.py /app/bot.py
CMD python /app/bot.py