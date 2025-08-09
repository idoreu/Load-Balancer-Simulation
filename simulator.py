#!/usr/bin/env python3

import random
import time
import heapq


def load_balancer_simulation(simulation_time, servers_num, arrival_rate, probabilities, queues, service_rates):
    random.seed(time.time())
    current_time = 0.0
    event_list = []
    servers  = []

    total_service_time = 0.0
    total_wait_time = 0.0
    customers_served = 0
    customers_rejected = 0

    T_end = 0.0

    ARRIVAL = 1
    DEPARTURE = 2

    # Allocate all server's resaurces
    for i in range(servers_num):
        servers.append({
            'queue' : [],
            'is_busy' : False,
            'current_customers_in_system' : 0,
        })
    balancer_id = -1

    # First request apearence
    if arrival_rate > 0:
        next_arrival = current_time + random.expovariate(arrival_rate)
        heapq.heappush(event_list, (next_arrival, ARRIVAL, balancer_id))
    
    # Run the simulation
    while current_time < simulation_time:
        if arrival_rate <= 0:
            break
        event_time, event_type, server_id = heapq.heappop(event_list)
        if event_time >= simulation_time:
            break
        current_time = event_time
        
        if event_type == ARRIVAL:
            next_arrival = current_time + random.expovariate(arrival_rate)
            heapq.heappush(event_list,(next_arrival, ARRIVAL, balancer_id))
            server_id = random.choices(population=range(servers_num),weights=probabilities, k=1)[0]
        chosen_server = servers[server_id]
        if event_type == ARRIVAL:
            if chosen_server['current_customers_in_system'] < queues[server_id]+1:
                chosen_server['current_customers_in_system'] +=1
                if not chosen_server['is_busy']:
                    chosen_server['is_busy'] = True
                    service_time = random.expovariate(service_rates[server_id])
                    total_service_time += service_time
                    heapq.heappush(event_list, (current_time + service_time, DEPARTURE, server_id))
                else:
                    chosen_server['queue'].append(current_time)
            else:
                customers_rejected += 1
        else:
            customers_served += 1
            chosen_server['current_customers_in_system'] -= 1
            if chosen_server['queue']:
                arrival_time = chosen_server['queue'].pop(0)
                wait_time = current_time - arrival_time
                total_wait_time += wait_time
                service_time = random.expovariate(service_rates[server_id])
                total_service_time += service_time
                heapq.heappush(event_list,(current_time+ service_time, DEPARTURE, server_id))
            else:
                chosen_server['is_busy'] = False
        T_end = current_time
    
    avarage_waite_time = 0.0
    avarage_service_time = 0.0
    if customers_served > 0:    
        avarage_waite_time = total_wait_time/customers_served
        avarage_service_time = total_service_time/customers_served
    
    return customers_served, customers_rejected, T_end, avarage_waite_time, avarage_service_time

def creat_a_list(type_of_list : str, default_value, size : int, cast_type=float):
    user_list = []
    user_answer = input(f"Do you want to pick the {type_of_list} values? (yes/no): ").strip().lower()
    if user_answer in ("yes" , "y"):
        print(f"Enter {type_of_list} for each server: ")
        for i in range(size):
            inp = input(f"{type_of_list} for server {i+1}: ")
            user_list.append(cast_type(inp) if inp else default_value)
    else:
        user_list = [default_value] * size
    return user_list

if __name__== "__main__":
    print("Welcome to the Load Balancer Simulation\n")
    simulation_time = float(input("Enter simulation time in seconds: "))
    servers_num = int(input("Enter number of servers: "))
    default_probability = (1.0 / servers_num) if servers_num > 0 else 0
    default_queue_size = 10
    default_service_rate = 2.0
    probabilities = []
    queues = []
    service_rates = []

    # Collecting probabilities, queues and service rates from user input
    probabilities_lst = input("Do you want to pick the probability values? (yes/no): ").strip().lower()
    if probabilities_lst in ("yes", "y"):
        sumup = 0.0
        for i in range(servers_num):
            inp = input(f"probability for server {i+1}: ")
            sumup += float(inp) if inp else 0.0
            probabilities.append(float(inp) if inp else default_probability)
        if sumup > 0.0:
            for i in range(servers_num):
                probabilities[i] /= sumup
    else:
        probabilities = [default_probability]*servers_num

    queue_lst = "queue size"
    queues = creat_a_list(queue_lst, default_queue_size, servers_num, int)
    user_service_rates_lst = "service rate"
    service_rates = creat_a_list(user_service_rates_lst, default_service_rate, servers_num, float)
    
    arrival_rate = 1.0  # Default arrival rate
    user_arival_rate = input("Do you want to pick the arrival rate? (yes/no): ").strip().lower()
    if user_arival_rate in ("yes", "y"):   
        arrival_rate = float(input("Enter the arrival rate (default is 1.0): ") or 1.0)
    # 


    customers_served, customers_rejected, T_end, avarage_waite_time, avarage_service_time = load_balancer_simulation(simulation_time, servers_num,arrival_rate, probabilities, queues, service_rates)
    print(f"\n results are:\n customers served - {customers_served},\n customers rejected - {customers_rejected},\n T_end - {T_end},")
    print(f" average wait time -  {avarage_waite_time},\n average_service_time - {avarage_service_time}\n")