To run Voucher api:

1. Make sure you have installed `docker/docker-compose` and `make`
2. Execute `make db.up` and wait for about 15 seconds.
    (Or check when the `make db.logs.follow` command shows `LOG:  database system is ready to accept connections`)
3. Execute `make up`. This will spin up the api and airflow
4. Now you need to trigger the Airflow dag. 
    You can either do it manually in Airflow UI or ~~execute `airflow.trigger-dag`~~(for some reason the cli in this docker setup doesn't behave properly).
5. Wait until the dag is done.(Maybe check the UI [here](http://localhost:8080/admin/airflow/graph?dag_id=voucher_calculation))
6. Make a test request by executing `make api.send-test-request`. The amount should be different from 0.