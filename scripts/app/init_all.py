import subprocess
import time

def run_script(script_name):
    process = subprocess.Popen(['python', script_name])
    return process

def main():
    # Run setup scripts
    subprocess.call(['python', 'database_setup.py'])
    subprocess.call(['python', 'minio_setup.py'])
    subprocess.call(['python', 'kafka_setup.py'])

    # Start consumers
    mariadb_consumer = run_script('mariadb_consumer.py')
    minio_consumer = run_script('minio_consumer.py')

    # Start the main bot
    bot_process = run_script('bot_main.py')

    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping all processes...")
        bot_process.terminate()
        mariadb_consumer.terminate()
        minio_consumer.terminate()

if __name__ == "__main__":
    main()