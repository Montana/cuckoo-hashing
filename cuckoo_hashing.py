from time import sleep


class Cuckoo:
    def __init__(self, size):
        self.size = size
        self.first = [None] * size
        self.second = [None] * size

    def add(self, key, val):
        from_second = (key, val, hash(key), hash(hash(key)))
        rounds = 0
        while True:
            rounds += 1
            if rounds > self.size:
                raise Exception(f"""Hash loop when inserting {key}""")
            first_index = from_second[2] % self.size
            from_first = self.first[first_index]
            self.first[first_index] = from_second
            if not from_first:
                break
            print(f"In primary   {from_second[0]}@{first_index} bumps {from_first[0]}")
            second_index = from_first[3] % self.size
            from_second = self.second[second_index]
            self.second[second_index] = from_first
            if not from_second:
                break
            print(f"In secondary {from_first[0]}@{second_index} bumps {from_second[0]}")
        print()

    def __str__(self):
        r = ""
        for i in range(self.size):
            f = self.first[i][0] if self.first[i] else " "
            s = self.second[i][0] if self.second[i] else " "
            r += f"{i:4}: {f:2}, {s:2}\n"
        return r

def main():
    table_size = 8
    cuckoo = Cuckoo(table_size)
    keys = " abcdefghijklmnopqrstuvwxyz"
    base = len(keys)
    for i in range(1, base**2):
        key = keys[i // base] + keys[i % base]
        print(f"Inserting {key}")
        try:
            cuckoo.add(key, i)
        except Exception as e:
            print()
            print(e)
            print(f"Table {(i-1)/(table_size*2):2.1%} full")
            break
        print(cuckoo)
        print()
        
if __name__ == "__main__":
    main()
