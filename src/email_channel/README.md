# Email Channel Service

The **Email Channel Service** is responsible for handling and sending email notifications.  
It runs as a standalone container but integrates with the backend via message brokers (Kafka/RabbitMQ).

## Features

- Sends email notifications based on domain events published by backend.  
- SMTP configuration via environment variables.  
- Can be scaled independently of other services.  


---

🔗 Back to [Root README](../../README.md)
