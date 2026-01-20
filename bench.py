import sys
from cli.arguments import parse_arguments
from core.validator import validate_url, validate_count
from core.benchmark import HTTPBenchmark
from utils.file_handler import load_hosts_from_file, save_output


def main():
    try:
        args = parse_arguments()
        
        if args.hosts:
            hosts = [h.strip() for h in args.hosts.split(',')]
        else:
            hosts = load_hosts_from_file(args.file)
        
        for host in hosts:
            if not validate_url(host):
                raise ValueError(f"Invalid URL format: {host}")
        
        try:
            count = validate_count(args.count)
        except ValueError as e:
            raise ValueError(str(e))
        
        print(f"Starting benchmark: {len(hosts)} host(s), {count} request(s) each...")
        benchmark = HTTPBenchmark(max_workers=10)
        benchmark.benchmark_hosts(hosts, count)
        
        output = benchmark.format_output()
        
        if args.output:
            save_output(output, args.output)
            print(f"Results saved to: {args.output}")
        else:
            print(output)
    
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nBenchmark interrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()