# schedsim_v2

The idea of SchedSim v2 is to rebuild from scratch the previous script from SchedSim (https://github.com/HEAPLab/schedsim). In particular, there is no more interest in the GUI, so it seeks to change the graphical interface for an output in text format with all the information about the result of the scheduling algorithm. Besides, the main goal is to implement all the scheduling algorithms seen in classes, which are: First-In-First-Out (FIFO), Shortest Job First (SJF), Shortest Remaining Time First (SRTF), Highest Response Ratio Next (HRRN), and Round Robin (RR). To develop this project it will still be used Python but PyQt will no longer be necessary. It should be noted that part of the code of SchedSim is reused in this implementation. It is correctly cited in the code itself.

## Documentation

The documentation is in the next link: https://github.com/tedroppelmann/schedsim_v2/blob/main/docs/Report.pdf

## Try to run

To run the application, it is necessary to run the next line in the terminal (located in the application folder). The line receives two arguments: the first is the name of the XML file with the tasks to be scheduled and the second is the name of the text file that will be generated with the final schedule.

```
python3 main.py <input_name.xml> <output_name.txt>
```

In this repository, there are some examples to test the implementation, like:

```
python3 main.py examples/Inputs/example_fifo.xml examples/Outputs/out.txt
```
```
python3 main.py examples/Inputs/example_rr.xml examples/Outputs/out.txt
```
```
python3 main.py examples/Inputs/example_hrrn.xml examples/Outputs/out.txt
```
