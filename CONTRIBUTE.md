# Contribution

If you want to contribute there's plenty of room for improvement in this tool!

Check whether an issue has previously addressed what you want to change. If not, feel free to open one and start the discussion!

## Add integrations with other AI clients

tiny-stories-generator has been implemented with extensibility in mind. At the moment, the main goal is to integrate with the batch APIs from different providers, as often synthetic data generation is not a task that requires low latency and usually needs large volumes of results. Using batch APIs is the best way to retrieve this while cutting costs for your data generation task.

You can add new clients by modifying the **src/clients.py** file. The project follows a simple Strategy design pattern, by extending the **BaseClient** defined in the file.

To manage the instantiation of different clients, a Factory pattern is implemented using the class **ClientFactory** present in **src/clients.py**. After creating your custom client, please register it in the factory to keep the instantiation simple for the rest of the scripts.

## Add custom metrics for evaluation

New custom metrics can be added to the **src/metrics.py** file so they can be referenced later. You can new metrics if they follow the mlflow style implementation.

## Other contributions

I believe every project has the chance to improve over time, and that the ways things are designed can change to better versions. If you have any other suggestion to improve this tool or want to contribute with something else, feel free to open the discussion!



