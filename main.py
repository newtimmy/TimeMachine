import time

def tmutil():
    import sys
    import subprocess

    tmstatus = subprocess.check_output(['tmutil','status'])
    tmstatus = tmstatus.splitlines()

    payload = {}
    Running = ""
    Percent = ""

    for line in tmstatus:
        ## clean up line data by stripping extraneous characters
        j = str(line)
        j = j.lstrip("b'")
        j = j.rstrip("';")
        j = j.strip()

        # Determine if there is an active Time Machine Backup in process
        if j.startswith("Running"):
            j = j.lstrip("Running = ")
            Running = int(j)
            payload["Running"] = Running

        # Exit if no active Time Machine Backup is in process
        if Running == 0:
            break

        # Get data on the active backup if there is one in process
        if Running == 1:
            tmstatus2 = subprocess.check_output(['tmutil', 'status'])
            tmstatus2 = tmstatus2.splitlines()
            for line2 in tmstatus2:
                k = str(line2)
                k = k.lstrip("b'")
                k = k.rstrip("';")
                k = k.strip()

                if k.startswith("BackupPhase"):
                    payload["BackupPhase"] = k.lstrip("BackupPhase = ")

                if k.startswith("ClientID"):
                    k = k.lstrip("ClientID = \"")
                    k = k.rstrip("\"")
                    payload["ClientID"] = k

                if k.startswith("DateOfStateChange"):
                    k = k.lstrip("DateOfStateChange = \"")
                    k = k.rstrip("\"")
                    payload["DateOfStateChange"] = k

                if k.startswith("DestinationID"):
                    k = k.lstrip("DestinationID = \"")
                    k = k.rstrip("\"")
                    payload["DestinationID"] = k

                if k.startswith("DestinationMountPoint"):
                    k = k.lstrip("DestinationMountPoint = \"")
                    k = k.rstrip("\"")
                    payload["DestinationMountPoint"] = k

                if k.startswith("Percent"):
                    k = k.lstrip("Percent = \"")
                    k = float(k.rstrip("\""))
                    k = k * 100
                    k = format(k, '.2f')
                    payload["Percent"] = k

                if k.startswith("Stopping"):
                    k = k.lstrip("Stopping = ")
                    payload["Stopping"] = k

                # Get even more data on the active backup if available
                if Percent != -1:
                    if k.startswith("NumberOfChangedItems"):
                        k = k.lstrip("NumberOfChangedItems = ")
                        payload["NumberOfChangedItems"] = k

                    if k.startswith("TimeRemaining"):
                        k = k.lstrip("TimeRemaining = ")
                        payload["TimeRemaining"] = k

                    if k.startswith("\"_raw_totalBytes\""):
                        k = k.lstrip("\"_raw_totalBytes\" = ")
                        k = float(k.rstrip("\""))
                        k = k * 100
                        k = format(k, '.2f')
                        payload["_raw_totalBytes"] = str(k) + "%"

                    if k.startswith("bytes"):
                        k = k.lstrip("bytes = ")
                        payload["bytes"] = k

                    if k.startswith("totalBytes"):
                        k = k.lstrip("totalBytes = ")
                        payload["totalBytes"] = k

                    if k.startswith("files"):
                        k = k.lstrip("files = ")
                        payload["files"] = k

                    if k.startswith("totalFiles"):
                        k = k.lstrip("totalFiles = ")
                        payload["totalFiles"] = k

                    if k.startswith("\"_raw_Percent\""):
                        k = k.lstrip("\"_raw_Percent\" = ")
                        k = float(k.rstrip("\""))
                        k = k * 100
                        k = format(k, '.2f')
                        payload["_raw_Percent"] = str(k)
            break

    if not bool(payload):
        return (payload)
    else:
        this_dict = {"Percent": "Backup is over"}
        #print(this_dict)
        return this_dict

while True:

    time.sleep(1)
    percent = tmutil()["Percent"]
    p1 = percent
    time.sleep(1)
    percent = tmutil()["Percent"]
    p2 = percent
    if percent != "Backup is over":
        print("Percentage:" + str(percent) + " Velocity: " + str(float(p2) - float(p1)))
    else:
        print("Backup over or not started yet")
