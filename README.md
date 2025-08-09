# Load Balancer Simulation

This project simulates a load balancer distributing requests to multiple servers, each with its own queue and service rate. 
The simulation is interactive and allows you to customize all key parameters.

## Features

- **Interface** for customisable simulation parameters 
- **Statistics**: 
        - components served
        - components rejected
        - average wait time
        - average service time
        - simulation end time
- **Poisson distribution for arrival time**
- **exponantially distributed service time**

## Requirements

- Python 3.x (tested with Python 3.7+)
- No external dependencies

## How to Run

1. Clone or download this repository.
2. Open a terminal in the project directory.
3. Run the simulation:
        >python simulator.py

## Example Usage

When you run the program, you will see prompts like:

Welcome to the Load Balancer Simulation

Enter simulation time in seconds: 100
Enter number of servers: 3
Do you want to pick the probability values? (yes/no): no
Do you want to pick the queue size values? (yes/no): no
Do you want to pick the service rate values? (yes/no): no
Do you want to pick the arrival rate? (yes/no): no

results are:
 customers served - 98,
 customers rejected - 0,
 T_end ~ 95.3,
 average wait time ~  0.068,
 average_service_time ~ 0.53

 <img width="855" height="379" alt="image" src="https://github.com/user-attachments/assets/c8f49baa-b1c3-4f42-b668-26006462f8ee" />


Alternatively you can answer "yes" to any of the parameter questions to enter custom values for each server.

## Parameter Descriptions

- **Simulation time**: Total time (in seconds) to run the simulation.
- **Number of servers**: How many servers the load balancer will distribute requests to.
- **Probabilities**: The probability that a new request is assigned to each server. If you enter custom values, they will be normalized to sum to 1.
- **Queue sizes**: Maximum number of requests each server can hold (including the one being served).
- **Service rates**: The average rate at which each server processes requests (higher means faster).
- **Arrival rate**: The average rate at which new requests arrive.

---

## Output

After the simulation, you will see:

- **Customers served**: Number of requests successfully processed.
- **Customers rejected**: Number of requests dropped due to full queues.
- **T_end**: Time at which the simulation ended.
- **Average wait time**: Average time a customer spent waiting in a queue.
- **Average service time**: Average time a customer spent being served.

---

## Customization

You can modify the code to add more features, such as:
- Different load balancing algorithms
- Logging to a file
- Visualization of queue lengths over time

---

## License

This project is provided for educational purposes.

---

## Author

[Your Name Here]
