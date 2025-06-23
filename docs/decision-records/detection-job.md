# Detection Execution as Queued Job #

## Revisions

- 23/06/2025: Initial draft
  - Aran Moncusi Ramirez

## Context

The detection algorithm could be computationally intensive in voice detection. It involves high CPU usage during
execution. Triggering this algorithm directly through synchronous API calls can cause several operational issues:

* Long response times, often exceeding the typical HTTP timeout limits.
* High risk of API gateway failures under load due to thread blocking or resource exhaustion.
* Lack of fault tolerance and observability for retry mechanisms and execution tracking.

Due to these potential issues, the need arose to decouple the execution of the detection logic from the API
request/response lifecycle.

## Considerations

* CPU-bound processing: Running the detection algorithm inline with HTTP requests ties up server resources and limits
  scalability.
* Timeout constraints: Synchronous API calls are subject to timeout limitations, which can lead to incomplete or failed
  executions.
* Scalability: Handling concurrent detection jobs in real-time places strain on application servers, requiring
  horizontal scaling for responsiveness.
* Observability and retry-ability: Without a job manager, failures are difficult to trace and recover from

## Decision

### Detection Algorithm Execution via Asynchronous Job Queue through the CommandExecutor interface.

We will execute the detection algorithm as a background task, managed through a RabbitMQ-based task queue system.

#### Why?
High CPU-demand operations are best handled outside the HTTP request lifecycle. By offloading these jobs to a background
queue:

* We avoid blocking API threads and stay within HTTP timeout limits.
* We gain greater control over task execution (e.g., retries, prioritization, delayed processing).
* We can scale consumers independently based on system load and processing requirements.
* We improve system reliability, as queue-based architectures decouple task initiation from execution, reducing surface
  area for failure during API requests.

## Consequences

* We introduce operational complexity by managing a job queue and workers, including monitoring and alerting.
* Developers must ensure job idempotency and proper error handling to avoid duplicate or failed executions.
* Users of the API must adapt to asynchronous response patterns (e.g., polling or webhooks for results).
* Improved system robustness, performance, and scalability for CPU-heavy algorithm execution.
