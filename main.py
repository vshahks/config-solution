import os
import signal
import sys
import time
import threading

ExtensionName = os.path.basename(sys.argv[0])
PrintPrefix = f"[{ExtensionName}] "

def signal_handler(signum, frame, ctx):
    print(f"{PrintPrefix} Received signal {signum}")
    print(f"{PrintPrefix} Exiting")
    ctx['cancelled'] = True

def main():
    global extension_client
    ctx = {'cancelled': False}
    signal.signal(signal.SIGTERM, lambda signum, frame: signal_handler(signum, frame, ctx))
    signal.signal(signal.SIGINT, lambda signum, frame: signal_handler(signum, frame, ctx))

    aws_lambda_runtime_api = os.getenv("AWS_LAMBDA_RUNTIME_API")
    extension_client = ExtensionClient(f"http://{aws_lambda_runtime_api}/2020-01-01/extension")

    res, err = extension_client.register(ctx, "extension_name")
    if err:
        raise Exception(err)
    print(f"{PrintPrefix} Register response: {pretty_print(res)}")

    init_cache_extensions()

    threading.Thread(target=start_http_server, args=("4000",)).start()

    process_events(ctx)

if __name__ == "__main__":
    main()