up:
	docker-compose up -d 

down:
	docker-compose down

api.up:
	docker-compose up -d --build api 

api.send-test-request:
	curl -X GET -H "Content-type: application/json" -d '{"customer_id": 123, "country_code": "Peru", "last_order_ts": "2018-05-03 00:00:00", "first_order_ts": "2017-05-03 00:00:00", "total_orders": 3, "segment_name": "recency_segment" }' "http://localhost:5000/segment/amount"

db.up:
	docker-compose up -d database

db.logs.follow:
	docker-compose logs -f database

airflow.up:
	docker-compose up -d airflow

airflow.trigger-dag:
	docker-compose exec airflow airflow unpause voucher_calculation
	docker-compose exec airflow airflow trigger_dag voucher_calculation