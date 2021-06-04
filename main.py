import json, time, statistics, math, config as c, mailer
from boltiot import Bolt

bolt = Bolt(c.api_key, c.device_id)
dataset = []

def z_score(dataset, frame, factor):
	mean = statistics.mean(dataset)
	variance = 0

	if len(dataset) < frame: # return mean in case of less data for the time being
		return mean, mean

	if len(dataset) > frame:
		del dataset[0:len(dataset)-frame]

	for data in dataset:
		variance += math.pow(data - mean, 2)

	score = factor * math.sqrt(variance / frame)
	upper_bound = dataset[frame-1]+score
	lower_bound = dataset[frame-1]-score

	return upper_bound, lower_bound


def sensor_data(pin):
	resp = bolt.analogRead(pin)
	data = json.loads(resp)
	alertsent = False

	if data['success'] != 1:
		message = "An error occurred while reading sensor input.\n"
		message += f"Error: {data['value']}\n"
		message += f"Entering cooldown mode for {c.cooldown}s\n"
		message += resp
		alert("🛑 Herald is unable to communicate 🛑", message)
		time.sleep(c.cooldown)

		return 0

	try:
		return int(data['value'])
	except Exception as ex:
		message = "An error occurred while parsing sensor input.\n"
		message += f"Value: {data['value']}\n"
		message += f"Exception: {ex}\n"
		alert("⚠ Herald is unable to communicate ⚠", message)

	return 0


def alert(subject, message):
	print(message)
	mailer.send(c.smtp_server, c.sender_email, c.recipients, 
	  subject, message, c.sender_password, c.sender_name)
	print(f"Alert sent to {c.recipients}")


def log(reading, bounds):
	print(f"Reading: {reading}, Bounds: {bounds}")


def verify_dataset(reading):
	if len(dataset) > c.frame_size:
		return
	while len(dataset) <= c.frame_size:
		print(f"Collecting data points {len(dataset)}/{c.frame_size}... Readings: {dataset}", end="\r")
		dataset.append(reading)
		time.sleep(c.interval)
		reading = sensor_data("A0")
	print("\t\t\t\t\t\t\t\t\t... done")


def run(reading):
	if reading == 0:
		return
	verify_dataset(reading)
	(upper_bound, lower_bound) = z_score(dataset, c.frame_size, c.factor)
	dataset.append(reading)
	log(reading, (upper_bound, lower_bound))

	subject = "⚠🚨 Intrusion Alert! Herald has detected an issue 🚨⚠"

	if reading > upper_bound:
		alert(subject, "The system has detected sudden change in proximity of objects which could be a sign of tempering the system. Caution is advised.")
	elif reading < lower_bound:
		alert(subject, "The system has detected an anomaly which could be a sign of intrusion. Caution is advised.")

	time.sleep(c.interval)


while True:
	run(sensor_data("A0"))
