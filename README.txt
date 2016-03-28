Run program:
   -> ./knapsack-dp.py -c config.json

Run tests:
   -> cd tests
   -> ./tests_run.py

Observations:
   -> The configuration file 'config.json' has the following format:
         -> The field 'products/file_path': it points to a CSV file with the products details
         -> The field 'products/amount_fields': it says the amount of fields with which is formatted the CSV file
         -> The field 'container/volume_length': it says the the knapsack 's length
         -> The field 'container/volume_width': it says the the knapsack 's width
         -> The field 'container/volume_height': it says the the knapsack 's height
   -> The CSV file with the products details has the following format:
         -> product ID, price, length, width, height, weight
   -> Profiling:
         -> In a Lenovo laptop (Ideapad Z580) with an Intel Core i7-3612QM CPU @2.10GHz*8, 7.7GiB, Ubuntu 15.10 64bits, 
            and Python 2.7.11 the call to "./knapsack-dp.py -c config.json" took 4.30 minutes to complete
         -> In order to profile the application:
               -> Install "line_profiler":
                     -> pip install line_profiler
               -> In "knapsack-dp.py" decorate the function "fillTable" with @profile
               -> Call "knapsack-dp.py" with:
                     -> kernprof -l -v knapsack-dp.py -c config.json
