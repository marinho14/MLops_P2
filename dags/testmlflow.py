import mlflow

mlflow.set_tracking_uri("http://localhost:5000")
mlflow_name = f"proyecto2model"
mlflow.set_experiment(mlflow_name)
desc = "modelo del proyecto 2"
with mlflow.start_run(run_name="run1", description=desc) as run:
    mlflow.autolog(log_model_signatures=True, log_input_examples=True)
    model_info = mlflow.sklearn.log_model(
        sk_model=,
        artifact_path=mlflow_name,
        input_example=,
        registered_model_name=mlflow_name,
    )
    print('tracking uri:', mlflow.get_tracking_uri())
    print('artifact uri:', mlflow.get_artifact_uri())
    print("model_uri", model_info.model_uri)
