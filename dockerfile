FROM python:3.12.8

WORKDIR /code/

COPY ./.env /code/.env
COPY ./main.py /code/main.py
COPY ./auth/* /code/auth/
COPY ./common/* /code/common/
COPY ./diff_analysis/* /code/diff_analysis/
COPY ./dash_area_info/* /code/dash_area_info/
COPY ./total_analysis/* /code/total_analysis/

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

EXPOSE 8892

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8892", "--reload"]
