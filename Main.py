class Flights:
    def  __init__(self,maxsize=5):
        self._maxsize=maxsize
        self._available=0
        self._array = [None] * self._maxsize
        self.flight_det={}

    def __len__(self):
        return self._available
    
    def __getitem__(self,index):
        if not 0 <= index < self._available:
            raise IndexError('Index out of bounds\nflight not avialable ')
        return self._array[index]

    def __setitem__(self, index, value):
        if not 0 <= index < self._available:
            raise IndexError('Index out of bounds\nflight not avialable')
        self._array[index] = value
    
    def append(self, value,flight_size,eco_seats,pre_eco_seats,bus_seats):
        if flight_size!=eco_seats+pre_eco_seats+bus_seats:
            raise ValueError('all seats')
        if value in self.flight_det:
            raise ValueError(f"Flight '{value}' is already added. Cannot add again.")
        if self._available == self._maxsize:
            self._resize(2 * self._maxsize) # when array is full, double the maxsize
        self._array[self._available] = value
        self._available += 1
        self.flight_det[value] = {} 
        self.flight_det[value] = arr_flight_seats(value, flight_size,eco_seats,pre_eco_seats,bus_seats,self)

    def insert(self, index, value,flight_size,eco_seats,pre_eco_seats,bus_seats):
        if not 0 <= index <= self._available:
            raise IndexError('Index out of bounds')
        if self._available == self._maxsize:
            self._resize(2 * self._maxsize)
        
        for i in range(self._available, index, -1):
            self._array[i] = self._array[i-1]
        
        self._array[index] = value
        self._available += 1
        self.flight_det[value] = arr_flight_seats(value, flight_size,eco_seats,pre_eco_seats,bus_seats)

    def remove(self, index):
        if self._available==0:
            raise IndexError('Index Out Of Bounds')
        if not 0 <= index < self._available:
            raise IndexError('Index out of bounds')
        
        for i in range(index, self._available - 1):
            self._array[i] = self._array[i+1]
        
        self._available -= 1
        self._array[self._available] = None

        if 0 < self._available < self._maxsize // 4:
            self._resize(self._maxsize // 2) # when array is less than 25% full, half the maxsize

    def __str__(self):
        return '[' + ', '.join(str(self._array[i]) for i in range(self._available)) + ']'

    # def __iter__(self):
    #     for i in range(self._available):
    #         yield self._array[i]

    def _resize(self, new_maxsize):
        new_array = [None] * new_maxsize

        for i in range(self._available):
            new_array[i] = self._array[i]

        self._array = new_array
        self._maxsize = new_maxsize

    def clear(self):
        self._array = [None] * self._maxsize
        self._available = 0

    def search(self,value):
        for i in range(0,self._available):
            if self._array[i]==value:
                return print("index is:",i) 
        return  "Flight not found"
    
    def assign_seat(self, flight_value, passenger_name,seat_type):
        return self.flight_det[flight_value].assign_seat(flight_value,passenger_name,seat_type)

def mysetarr(obj, attr_name, value):
    obj.__dict__[attr_name] = value
def mygetarr(obj, attr_name, default=None):
    return obj.__dict__.get(attr_name, default)
def my_hasattr(obj, attr_name):
    try:
        mygetarr(obj, attr_name)  
        return True 
    except AttributeError:
        return False
def StringCheck(obj, class_type):
    return type(obj) == class_type 
def my_enumerate(iterable, start=0):
    index = start
    for item in iterable:
        yield index, item
        index += 1
def my_len(iterable):
    count = 0
    for _ in iterable:
        count += 1
    return count

    

class arr_flight_seats:
    def __init__(self,flight_value,total_seats,eco_seats,pre_eco_seats,bus_seats,e):
        if not StringCheck(flight_value, str):
            raise ValueError("Flight must be a string representing flight name.")
        if flight_value not in e.flight_det:
            raise ValueError(f"Flight '{flight_value}' not found. Please add it using 'append()' in Flights class first.")
        self.flight_value = flight_value
        self.total_seats = total_seats
        mysetarr(self, f"arr_{flight_value}", [None] * total_seats)
        self.economy = eco_seats
        self.premuim_economy = pre_eco_seats
        self.business = bus_seats

        self.business_range = (0, bus_seats - 1)
        self.premium_economy_range = (bus_seats, bus_seats + pre_eco_seats - 1)
        self.economy_range = (bus_seats + pre_eco_seats, total_seats - 1)


    def assign_seat(self,flight_value,passenger_name,seat_type):
        flight_val = f"arr_{flight_value}"
        if not my_hasattr(self, flight_val): 
            raise ValueError(f"Flight {flight_value} does not exist.")
        if seat_type not in ["economy", "premium_economy", "business"]:
            raise ValueError(f"Flight {flight_value} does not have {seat_type}")
        seats = mygetarr(self, flight_val) 
        if seat_type == "business":
            start, end = self.business_range
        elif seat_type == "premium_economy":
            start, end = self.premium_economy_range
        else:
            start, end = self.economy_range
        for i in range(start, end + 1):
            if seats[i] is None:
                seats[i] = passenger_name
                return print(f"Seat assigned to {passenger_name} in {flight_value} Seat {i + 1} ({seat_type})")

        return print(f"No available {seat_type} seats on flight {flight_value}, You will be in the standby list.")
        
    
class Passenger_det_Heap:
    def __init__(self, max_size,flight_value):
        self.heap = []
        self.max_size = max_size
        self.flights=Flights()
        mysetarr(self,f"dic_{flight_value}",{})
        

    def insert(self,flight_value,priority,passenger_name,seat_type):
        if my_len(self.heap) >= self.max_size:
            raise OverflowError("Heap is at maximum size")
        
        self.append((priority, passenger_name))
        self._heapify_up(my_len(self.heap) - 1)
        flight_dic_name = f"dic_{flight_value}"  
        flight_dic = mygetarr(self, flight_dic_name, {})  # Retrieve dictionary or create a new one
        flight_dic[passenger_name] = seat_type  # Assign seat type to passenger
        mysetarr(self, flight_dic_name, flight_dic) 

    def remove_passenger(self, passenger_name):
        for index, (_, name) in my_enumerate(self.heap):
            if name == passenger_name:
                self.heap[index], self.heap[-1] = self.heap[-1], self.heap[index]
                removed_passenger = self.pop()
                self._heapify_down(index)
                self._heapify_up(index)
                return removed_passenger
        return None  

    def remove_highest_priority(self):
        if not self.heap:
            return None

        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        removed_passenger = self.pop()
        self._heapify_down(0)
        #need to connect from flight_dic [pname,seat type] to assaign_seat
        return removed_passenger

    def _heapify_up(self, index):
        parent_index = (index - 1) // 2
        while index > 0 and self.heap[index][0] < self.heap[parent_index][0]:
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            index = parent_index
            parent_index = (index - 1) // 2

    def _heapify_down(self, index):
        size = my_len(self.heap)
        while index < size:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if left < size and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < size and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right

            if smallest != index:
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                index = smallest
            else:
                break
    def append(self, name):
        if my_len(self.heap) >= self.max_size:
            raise OverflowError("Heap is at maximum size")
        new_heap = [None] * (my_len(self.heap) + 1)
        for i in range(my_len(self.heap)):
            new_heap[i] = self.heap[i]
        new_heap[my_len(self.heap)] = name
        self.heap = new_heap
    
    def pop(self):
        if not self.heap:
            return None
        new_heap = [None] * (my_len(self.heap) - 1)
        removed_element = self.heap[-1]
        for i in range(my_len(self.heap) - 1):
            new_heap[i] = self.heap[i]
        self.heap = new_heap
        return removed_element
    
    def view_heap(self):
        return print(sorted(self.heap))  # Sorted to view passengers in priority order

        

f=Flights(5)
f.append("indigo1",138,66,42,30)
f.append("indigo2",138,66,42,30)
f.append("indigo3",138,66,42,30)
f.append("indigo4",138,66,42,30)
print(f._array)
f.append("indigo5",138,66,42,30)
print(f._array)
print(f._available)
f.append("indigo6",138,66,42,30)
print(f._array)
print(f._available)
g=f.__getitem__(3)
print(g)
print(f.__getitem__(3))
print(f[3])
f.__setitem__(3,"airindia")
print(f._array)
f.clear()
#f.remove(0)
#a=arr_flight_seats("indigo7",150,70,50,30,f)
#a=arr_flight_seats("1indigo",150,70,50,30,f)
#a=arr_flight_seats(9,150,70,50,30,"e")
#a = f.flight_det["indigo3"]
#a.assign_seat("indigo3","jatin","econmy")
#f.search("indigo")
#P=Passenger_det_Heap(138,"indigo")   
#P.insert("indigo",2,"rakesh","economy")
#P.insert(23,"raesh")
#P.insert(4,"akeh")
#P.insert(9,"rkesh")
#P.view_heap()
#f.assign_seat("indigo","jatin","economy")
#f.assign_seat("indigo","rakesh","business")
