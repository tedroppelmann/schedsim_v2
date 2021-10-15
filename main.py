import SchedIO

if __name__ == "__main__":
    scheduler = SchedIO.import_file('example_hrrn.xml')
    scheduler.execute()
