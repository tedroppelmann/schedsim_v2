import SchedIO

if __name__ == "__main__":
    scheduler = SchedIO.import_file('example_sjf.xml')
    scheduler.execute()
