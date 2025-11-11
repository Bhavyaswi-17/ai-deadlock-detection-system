from rag_visualizer import RagVisualizer
class DeadlockDetection():
    def main(self):
        #number of processes and resources
        processes = int(input("Enter number of processes: "))
        resources = int(input("Enter number of resources: "))
        #enter available resources
        available = []
        print("Enter available resources: ")    
        for i in range(resources):
            available.append(int(input(f"Resource R{i+1}: ")))
        #Maximum need matrix
        max_matrix = []
        print("\nEnter Max matrix:")
        for i in range(processes):
            row = []
            print(f"Process P{i+1}: ")
            for j in range(resources):
                row.append(int(input(f"Max need of R{j+1}: ")))
            max_matrix.append(row)
        #Allocation matrix
        allocation_matrix = []
        print("\nEnter Allocation matrix:")
        for i in range(processes):
            row = []
            print(f"Process P{i+1}: ")
            for j in range(resources):
                row.append(int(input(f"Allocated R{j+1}: ")))
            allocation_matrix.append(row)
         #need matrix calculation
        need_matrix = []
        for i in range(processes):
            row = []
            for j in range(resources):
                row.append(max_matrix[i][j] - allocation_matrix[i][j])
            need_matrix.append(row)
        #banker's algorithm to detect deadlock
        finish = [False] * processes
        safe_sequence = []
        while len(safe_sequence) < processes:
            allocated = False
            for i in range(processes):
                if not finish[i]:
                    can_allocate = True
                    for j in range(resources):
                        if need_matrix[i][j] > available[j]:
                            can_allocate = False
                            break
                    if can_allocate:
                        for j in range(resources):
                            available[j] += allocation_matrix[i][j]
                        finish[i] = True
                        safe_sequence.append(i)
                        allocated = True
            if not allocated:
                break
        #determine deadlocked processes
        deadlocked_processes = [i for i in range(processes) if not finish[i]]
        #
        if len(deadlocked_processes) == 0:
            print("\n No Deadlock Detected!")
            #safe sequence output
            print("Safe Sequence:", " → ".join([f"P{i+1}" for i in safe_sequence]))
            # Draw Resource Allocation Graph
            RagVisualizer(processes, resources,allocation_matrix,max_matrix,available).visualize()
        else:
            print("\n Deadlock Detected!")
            print("Deadlocked processes:", ", ".join([f"P{i+1}" for i in deadlocked_processes]))
            # Draw Resource Allocation Graph with deadlock highlighted
            RagVisualizer(processes,resources,allocation_matrix,max_matrix,available,deadlocked_processes).visualize()
# Run the progrom
if __name__ == "__main__":
    DeadlockDetection().main()

