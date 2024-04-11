FROM python
WORKDIR /Finance_Tracker
COPY requirements.txt /Finance_Tracker
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP=app.py
CMD ["python", "app.py", "--host=0.0.0.0"]