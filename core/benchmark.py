import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Tuple
from statistics import mean

import httpx


class HTTPBenchmark:
    def __init__(self, max_workers: int = 10, timeout: int = 10):
        self.max_workers = max_workers
        self.timeout = timeout
        self.results: Dict[str, List[float]] = defaultdict(list)
        self.stats: Dict[str, Dict] = {}
    
    def make_request(self, host: str) -> Tuple[str, float, int, bool]:
        try:
            start = time.time()
            
            if hasattr(httpx, 'get'):  
                response = httpx.get(host, timeout=self.timeout)
            else:  
                import httpx as hx
                with hx.Client() as client:
                    response = client.get(host, timeout=self.timeout)
            
            elapsed = (time.time() - start) * 1000 
            status_code = response.status_code
            
            is_error = 400 <= status_code < 600
            return host, elapsed, status_code, is_error
            
        except Exception as e:
            return host, 0, 0, True
    
    def benchmark_hosts(self, hosts: List[str], count: int) -> None:
        total_requests = len(hosts) * count
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {}
            for host in hosts:
                for _ in range(count):
                    future = executor.submit(self.make_request, host)
                    futures[future] = host
            
            for future in as_completed(futures):
                host, elapsed, status_code, is_error = future.result()
                
                if elapsed > 0:
                    self.results[host].append(elapsed)
                else:
                    self.results[host].append(None)
        
        self._calculate_statistics()
    
    def _calculate_statistics(self) -> None:
        for host, times in self.results.items():
            valid_times = [t for t in times if t is not None]
            error_count = len(times) - len(valid_times)
            
            success_count = len(valid_times)
            failed_count = 0 
            
            self.stats[host] = {
                'host': host,
                'total': len(times),
                'success': success_count,
                'failed': failed_count,
                'errors': error_count,
                'min': min(valid_times) if valid_times else 0,
                'max': max(valid_times) if valid_times else 0,
                'avg': mean(valid_times) if valid_times else 0,
            }
    
    def format_output(self) -> str:
        output = []
        output.append("=" * 70 )
        output.append("HTTP Server Benchmark Results")
        output.append("=" * 70)
        
        for host, stats in self.stats.items():
            output.append("")
            output.append(f"Host: {stats['host']}")
            output.append("-" * 70)
            output.append(f"  Success:  {stats['success']}")
            output.append(f"  Failed:   {stats['failed']}")
            output.append(f"  Errors:   {stats['errors']}")
            output.append(f"  Min:      {stats['min']:.2f} ms")
            output.append(f"  Max:      {stats['max']:.2f} ms")
            output.append(f"  Avg:      {stats['avg']:.2f} ms")
        
        output.append("")
        output.append("=" * 70)
        
        return "\n".join(output)