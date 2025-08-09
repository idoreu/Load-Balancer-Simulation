#!/usr/bin/env python3

import random
import sys
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


if __name__== "__main__":
    simulation_time = float(sys.argv[1])
    servers_num = int(sys.argv[2])
    probabilities = []
    queues = []
    service_rates = []
    arrival_rate = float(sys.argv[servers_num +3])
    for n in range(servers_num):
        probabilities.append(float(sys.argv[n+3]))
        queues.append(int(sys.argv[n + servers_num + 4])+1)
        service_rates.append(float(sys.argv[n + 2*servers_num + 4]))
    customers_served, customers_rejected, T_end, avarage_waite_time, avarage_service_time = load_balancer_simulation(simulation_time, servers_num,arrival_rate, probabilities, queues, service_rates)
    print(f" results are:\n customers served - {customers_served},\n customers rejected - {customers_rejected},\n T_end - {T_end},")
    print(f" average waite time -  {avarage_waite_time},\n avarage_service_time - {avarage_service_time}\n")