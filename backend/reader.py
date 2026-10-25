import psycopg
import logging
import serial
from re import split
import time 
from sys import exit

logger = logging.getLogger("sensor_reader")
i = 0

logging.basicConfig(format="%(asctime)s | %(name)s | %(levelname)s | %(filename)s | %(message)s", datefmt="%H:%M:%S", level=logging.INFO)
with psycopg.connect("dbname=mydb user=salih") as conn:
    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE IF NOT EXISTS sensor_readings (
                        temp    REAL,
                        hum     REAL,
                        pres    REAL,
                        ts    TIMESTAMPTZ)
                """)
        while True:
            try:
                with serial.Serial('/dev/ttyACM0', 115200, timeout=10) as ser:
                    logger.info("Successfully connected")
                    i = 1
                    time.sleep(0.1)
                    logger.info("Resetting input buffer...")
                    ser.reset_input_buffer()
                    ser.readline()
                    while True:
                            p = ser.readline()
                            q = p.decode("utf-8", errors="ignore").strip()
                            res = split(r'[=,]', q)
                            try:
                                temp, hum, pres = res[1],res[3],res[5]
                            except (IndexError, ValueError, UnicodeDecodeError) as e:
                                logger.warning(f"Skipping decoding error : {e}")
                                continue 
                            cur.execute("INSERT INTO sensor_readings(temp,hum,pres,ts) VALUES(%s,%s,%s,%s)",
                                        (temp, hum, pres, time.ctime()))
                            
                            cur.execute("SELECT * FROM sensor_readings ORDER BY ts DESC LIMIT 1 OFFSET 0")

                            for row in cur:
                                logger.info(f"NEW ROW ADDED | temp : {row[0]}, hum : {row[1]}, pres : {row[2]}, time : {row[3]}")
                            
                            conn.commit()
            
            except serial.SerialException:
                logger.warning(f"No connection. Attempting to connect... {i}/10")
                time.sleep(1)
                i += 1
                if (i == 10):
                    logger.error('Failed to connect after 10 attempts.\nExiting...')
                    exit(1)
            except KeyboardInterrupt:
                logger.info("\nIntentional exit detected")
                exit(0)



